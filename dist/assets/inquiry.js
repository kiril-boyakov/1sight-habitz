(() => {
  const form = document.querySelector('#inquiry-form');
  if (!form) return;
  form.hidden = false;
  const kind = form.elements.kind;
  const message = form.elements.message;
  const submit = form.querySelector('button[type="submit"]');
  const status = form.querySelector('[role="status"]');
  const resetHint = () => {
    message.placeholder = kind.selectedOptions[0]?.dataset.hint || '';
  };
  kind.addEventListener('change', resetHint);
  resetHint();
  document.querySelectorAll('[data-inquiry-kind]').forEach(link => {
    link.addEventListener('click', () => {
      kind.value = link.dataset.inquiryKind;
      resetHint();
    });
  });

  let lastPayload = '';
  let requestId;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (submit.disabled || !form.reportValidity()) return;
    const payload = Object.fromEntries(new FormData(form));
    const signature = JSON.stringify(payload);
    if (signature !== lastPayload) {
      requestId = undefined;
      lastPayload = signature;
    }
    submit.disabled = true;
    status.textContent = form.dataset.sending;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      if (!requestId) {
        const bytes = crypto.getRandomValues(new Uint8Array(16));
        requestId = Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
      }
      const response = await fetch(form.action, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: JSON.stringify({...payload, id: requestId, lang: document.documentElement.lang}),
        signal: controller.signal,
      });
      const result = await response.json();
      if (!response.ok || result.accepted !== true) throw new Error('Request rejected');
      status.textContent = result.demo ? form.dataset.demo : form.dataset.success;
      form.reset();
      resetHint();
      lastPayload = '';
    } catch {
      status.textContent = form.dataset.error;
    } finally {
      clearTimeout(timeout);
      submit.disabled = false;
    }
  });
})();
