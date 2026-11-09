const manager = 'manager@herbits.lt';
const topics = {
  collab: 'Bendradarbiavimas su šefais ir restoranais',
  corporate: 'Restorano nuoma įmonei',
  bakery: 'Kepinių tiekimas',
  celebration: 'Asmeninė šventė',
};

function reply(status, body) {
  return Response.json(body, {status, headers: {'Cache-Control': 'no-store'}});
}

async function readBoundedJson(request) {
  const reader = request.body?.getReader();
  if (!reader) throw new Error('Missing body');
  const chunks = [];
  let total = 0;
  for (;;) {
    const {value, done} = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > 16384) {
      await reader.cancel();
      throw new Error('Body too large');
    }
    chunks.push(value);
  }
  return JSON.parse(await new Blob(chunks).text());
}

function parseFields(payload) {
  if (!payload || typeof payload !== 'object') return null;
  const {id, lang, kind} = payload;
  const clean = key => typeof payload[key] === 'string' ? payload[key].trim() : '';
  const name = clean('name');
  const email = clean('email');
  const message = clean('message');
  if (typeof id !== 'string' || !/^[a-f0-9]{32}$/.test(id) ||
      !['lt', 'en'].includes(lang) || !Object.hasOwn(topics, kind) ||
      !name || name.length > 120 || !message || message.length > 3000 ||
      email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return null;
  return {id, lang, kind, name, email, message};
}

async function notifyManager(env, data) {
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + env.RESEND_API_KEY,
      'Content-Type': 'application/json',
      'Idempotency-Key': 'habits-' + data.id,
    },
    body: JSON.stringify({
      from: env.INQUIRY_FROM,
      to: [manager],
      reply_to: data.email,
      subject: 'HABITS · ' + topics[data.kind],
      text: [topics[data.kind], data.name, data.email, '', data.message].join('\n'),
    }),
  });
  if (!response.ok) throw new Error('Delivery failed: ' + response.status);
  await env.INQUIRIES.prepare('UPDATE inquiries SET notified = 1 WHERE id = ?')
    .bind(data.id).run();
}

export async function onRequest({request, env, waitUntil}) {
  if (request.method !== 'POST') return reply(405, {error: 'POST required'});
  const origin = request.headers.get('Origin');
  if (origin && origin !== new URL(request.url).origin) return reply(403, {error: 'Forbidden'});
  if (request.headers.get('Content-Type')?.split(';')[0] !== 'application/json')
    return reply(415, {error: 'JSON required'});
  let data;
  try {
    data = parseFields(await readBoundedJson(request));
  } catch {
    return reply(400, {error: 'Invalid request'});
  }
  if (!data) return reply(422, {error: 'Invalid fields'});
  try {
    const db = env.INQUIRIES;
    const result = await db.prepare(
      'INSERT INTO inquiries (id, lang, kind, name, email, message) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO NOTHING',
    ).bind(data.id, data.lang, data.kind, data.name, data.email, data.message).run();
    let notified = false;
    if (!result.meta.changes) {
      const row = await db.prepare('SELECT * FROM inquiries WHERE id = ?').bind(data.id).first();
      if (!row || Object.keys(data).some(key => row[key] !== data[key]))
        return reply(409, {error: 'Request ID conflict'});
      notified = row.notified === 1;
    }
    if (!notified && env.RESEND_API_KEY && env.INQUIRY_FROM) {
      waitUntil(notifyManager(env, data).catch(() => console.error('Enquiry notification pending:', data.id)));
    }
    return reply(200, {accepted: true, demo: env.LOCAL_DEMO === '1'});
  } catch {
    return reply(503, {error: 'Inbox unavailable'});
  }
}
