// Local-only demo: serve the landing page and store enquiries in a private SQLite file.
import {createServer} from 'node:http';
import {DatabaseSync} from 'node:sqlite';
import {readFile, stat} from 'node:fs/promises';
import {createReadStream, mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {extname, join, resolve, sep} from 'node:path';
import {tmpdir} from 'node:os';
import {onRequest} from './functions/api/inquiries.js';

const root = fileURLToPath(new URL('.', import.meta.url));
const dist = resolve(root, 'dist');
const storage = process.env.HABITS_DEMO_DIR || join(tmpdir(), 'habits-demka-malinka');
mkdirSync(storage, {recursive: true, mode: 0o700});
const sqlite = new DatabaseSync(join(storage, 'inquiries.sqlite'));
sqlite.exec(await readFile(join(root, 'inquiry-schema.sql'), 'utf8'));
const inbox = {
  prepare(sql) {
    const stmt = sqlite.prepare(sql);
    return {bind(...values) {return {
      run: () => ({meta: {changes: stmt.run(...values).changes}}),
      first: () => stmt.get(...values),
    };}};
  },
};
const types = {'.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.webp': 'image/webp', '.woff2': 'font/woff2', '.ttf': 'font/ttf',
  '.jpg': 'image/jpeg', '.mp4': 'video/mp4', '.png': 'image/png', '.txt': 'text/plain'};

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://' + req.headers.host);
    if (url.pathname === '/api/inquiries') {
      const init = {method: req.method, headers: req.headers};
      if (req.method === 'POST') Object.assign(init, {body: req, duplex: 'half'});
      const response = await onRequest({request: new Request(url, init), env: {INQUIRIES: inbox, LOCAL_DEMO: '1'}});
      res.writeHead(response.status, Object.fromEntries(response.headers));
      return res.end(await response.text());
    }
    if (!['GET', 'HEAD'].includes(req.method)) {res.writeHead(405); return res.end();}
    let file = resolve(dist, '.' + decodeURIComponent(url.pathname));
    if (file !== dist && !file.startsWith(dist + sep)) {res.writeHead(403); return res.end();}
    if ((await stat(file)).isDirectory()) file = join(file, 'index.html');
    const size = (await stat(file)).size;
    res.writeHead(200, {'Content-Type': types[extname(file)] || 'application/octet-stream', 'Content-Length': size});
    if (req.method === 'HEAD') return res.end();
    createReadStream(file).on('error', () => res.destroy()).pipe(res);
  } catch {
    if (!res.headersSent) res.writeHead(404);
    res.end();
  }
}).listen(Number(process.env.PORT || 8765), '127.0.0.1', function () {
  console.log('HABITS demo: http://127.0.0.1:' + this.address().port + '/');
});
