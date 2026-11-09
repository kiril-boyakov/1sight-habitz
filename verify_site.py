"""Check generated routes, anchors, metadata and responsive asset references."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json, hashlib
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
class Document(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,name,attrs):self.tags.append((name,dict(attrs)))
menu=json.loads((ROOT/"src/menu.json").read_text())
menu_count=sum(len(group["items"]) for cat in menu["categories"] for group in cat["groups"])
docs={p:Document(p.read_text()) for p in DIST.rglob('index.html')}
fail=[]
for page,doc in docs.items():
 ids=[a['id'] for _,a in doc.tags if 'id' in a]
 if len(ids)!=len(set(ids)):fail.append(f'{page}: duplicate IDs')
 if sum(tag=='h1' for tag,_ in doc.tags)!=1:fail.append(f'{page}: H1 count')
 locale='en' if 'en' in page.relative_to(DIST).parts else 'lt'
 for tag,a in doc.tags:
  if tag=='img' and 'alt' not in a:fail.append(f'{page}: missing alt')
  refs=[a[k] for k in ['href','src','poster'] if k in a]
  if 'srcset' in a:refs.extend(v.strip().split()[0] for v in a['srcset'].split(','))
  if 'data-src' in a:refs.append(a['data-src'])
  for ref in refs:
   url=urlsplit(ref)
   if url.scheme or url.netloc:continue
   path=DIST/url.path.lstrip('/') if url.path else page
   if path.is_dir():path=path/'index.html'
   if not path.exists():fail.append(f'{page}: missing {ref}');continue
   if url.fragment and path.suffix=='.html':
    target=Document(path.read_text())
    if unquote(url.fragment) not in [x.get('id') for _,x in target.tags]:fail.append(f'{page}: missing anchor {ref}')
  if tag=='a' and 'habits.tablein.com' in a.get('href','') and a['href']!='https://habits.tablein.com/'+locale:fail.append(f'{page}: booking language')
 if 'menu' in page.relative_to(DIST).parts and sum(t=='article' and a.get('class')=='dish' for t,a in doc.tags)!=menu_count:fail.append(f'{page}: menu count')
 for name in ['canonical','alternate']:
  if not any(t=='link' and a.get('rel')==name for t,a in doc.tags):fail.append(f'{page}: missing {name}')
assert len(docs)==6,len(docs)
assert not fail,'\n'.join(fail)
gallery=json.loads((ROOT/'src/gallery.json').read_text())
assert {photo['kind'] for photo in gallery}=={'collab','corporate','bakery','celebration'}
assert len({photo['file'] for photo in gallery})==len(gallery), 'Gallery filenames repeat'
digests=[hashlib.sha256((DIST/'assets'/photo['file']).read_bytes()).hexdigest() for photo in gallery]
assert len(set(digests))==len(digests), 'Gallery photographs repeat'
image_data=json.loads((ROOT/'src/images.json').read_text())
category_images=[image_data[category['image']]['variants'][-1]['file'] for category in menu['categories']]
assert len(set(category_images))==len(category_images), 'Menu category photographs repeat'
print(f'PASS: six pages, {menu_count} menu items per language, localized booking links, anchors, alt text, metadata and responsive assets.')
