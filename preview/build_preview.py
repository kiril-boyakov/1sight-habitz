"""Package all six routes, fonts, styles and photographs in one offline preview."""
from pathlib import Path
import base64
import json
import mimetypes
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
OUTPUT = ROOT / 'preview' / 'HABITS-preview-v8.html'

assets = {}
images = json.loads((ROOT / 'src' / 'images.json').read_text())
photo_files = {v['file'] for image in images.values() for v in image['variants']}
photo_files.update(photo['file'] for photo in json.loads((ROOT / 'src/gallery.json').read_text()))
for path in (DIST / 'assets').iterdir():
    if path.suffix == '.ttf' or path.name in photo_files | {'wordmark.png', 'favicon.png', 'social.jpg', 'location-map.svg', 'habits-film.mp4'}:
        mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        assets['/assets/' + path.name] = (
            f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()
        )

css = (DIST / 'assets' / 'site.css').read_text().replace(
    "@import url('/assets/fonts.css');", (DIST / 'assets' / 'fonts.css').read_text()
) + (DIST / 'assets' / 'inquiry.css').read_text()
script = (DIST / 'assets' / 'site.js').read_text()
inquiry_script = """
const inquiry = document.querySelector('#inquiry-form');
if (inquiry) {
  inquiry.hidden = false;
  const kind = inquiry.elements.kind;
  const hint = () => { inquiry.elements.message.placeholder = kind.selectedOptions[0]?.dataset.hint || ''; };
  kind.addEventListener('change', hint);
  document.querySelectorAll('[data-inquiry-kind]').forEach(link => link.addEventListener('click', () => {
    kind.value = link.dataset.inquiryKind;
    hint();
  }));
  inquiry.addEventListener('submit', event => {
    event.preventDefault();
    inquiry.querySelector('[role="status"]').textContent = document.documentElement.lang === 'lt'
      ? 'Tai peržiūra. Dėl užklausos parašykite manager@habits.lt.'
      : 'This is a preview. To make an enquiry, email manager@habits.lt.';
  });
}
"""
bridge = """
document.addEventListener('click', event => {
  const link = event.target.closest('a');
  if (!link || !link.getAttribute('href')?.startsWith('/')) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  const target = link.getAttribute('href').split('#');
  const hash = target[1] || (link.hasAttribute('data-language') ? location.hash.slice(1) : '');
  parent.postMessage({habitsRoute: target[0], hash}, '*');
}, true);
"""

pages = {}
for path in DIST.rglob('index.html'):
    route = '/' + str(path.parent.relative_to(DIST)).replace('.', '')
    if not route.endswith('/'):
        route += '/'
    html = path.read_text()
    html = re.sub(r'<link[^>]*rel="stylesheet"[^>]*>', '', html)
    html = re.sub(r'<script[^>]*src="[^"]*"[^>]*></script>', '', html)
    html = re.sub(r'\s(?:srcset|sizes)="[^"]*"', '', html)
    html = html.replace('</head>', '<style>' + css + '</style></head>')
    html = html.replace('</body>', '<script>(()=>{' + script + inquiry_script + bridge + '})()</script></body>')
    pages[route] = html

payload = json.dumps({'assets': assets, 'pages': pages}, ensure_ascii=False).replace('</', '<\\/')
OUTPUT.write_text('''<!doctype html><html lang="lt"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>HABITS — preview</title>
<style>html,body,iframe{width:100%;height:100%;margin:0;border:0;display:block}body{background:#f5f2eb}</style>
</head><body><iframe id="preview" title="HABITS Vilnius"></iframe><script>
const bundle = ''' + payload + ''';
const frame = document.getElementById('preview');
function show(route, hash = '') {
  const template = bundle.pages[route];
  if (!template) return;
  const html = template.replace(/\\/assets\\/[A-Za-z0-9._-]+/g, path => bundle.assets[path] || path);
  frame.onload = () => {
    if (hash) frame.contentWindow.location.hash = hash;
  };
  frame.srcdoc = html;
}
addEventListener('message', event => {
  if (event.source === frame.contentWindow && typeof event.data?.habitsRoute === 'string') {
    show(event.data.habitsRoute, event.data.hash);
  }
});
show('/');
</script></body></html>''')
assert set(pages) == {'/', '/menu/', '/privacy/', '/en/', '/en/menu/', '/en/privacy/'}
assert all('/assets/' + name in assets for name in ['wordmark.png', 'font-0.ttf', 'hero-1080.webp'])
print(f'Packaged {len(pages)} routes and {len(assets)} embedded assets: {OUTPUT}')
