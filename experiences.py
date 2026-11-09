"""The event archive and four enquiry paths share one place on the homepage."""

from html import escape
from pathlib import Path
import json

GALLERY = json.loads((Path(__file__).resolve().parent / 'src/gallery.json').read_text())
CONTENT = {
    'lt': {
        'label': 'RENGINIAI IR PARTNERYSTĖS', 'title': 'Prie vieno stalo.',
        'categories': 'Pasirinkite, kas domina', 'cta': 'Pateikti užklausą',
        'paths': [
            ('collab', 'Šefams ir restoranams', 'Vakarienės keturiomis rankomis.',
             'Kartą per mėnesį į savo virtuvę kviečiame kitą šefą ar restoraną. Prie HABITS stalo jau susitikome su MOTÍF ir „Ugruzina“. Ką gamintume kartu su jumis?'),
            ('corporate', 'Įmonių renginiai', 'Visas HABITS jūsų komandai.',
             'Komandos vakarienė, susitikimas su klientais ar įmonės šventė. Galite rezervuoti visą restoraną. Parašykite, kurią dieną planuojate renginį ir kiek žmonių susirinks.'),
            ('bakery', 'Kepiniai verslui', 'Iš mūsų kepyklos į jūsų kavinę.',
             'Tiekiame HABITS kepinius kavinėms ir biurams. Tarp mūsų partnerių – Vilniaus kavinė „Strange Love“. Papasakokite, kur ir kaip dažnai norėtumėte gauti kepinių.'),
            ('celebration', 'Asmeninės šventės', 'Šiandien švenčiate jūs.',
             'Vestuvės, gimtadienis ar vakarienė su artimiausiais. Pasidalykite savo data, svečių skaičiumi ir tuo, kaip įsivaizduojate vakarą.'),
        ],
    },
    'en': {
        'label': 'EVENTS & PARTNERSHIPS', 'title': 'Around one table.',
        'categories': 'Choose what brings you here', 'cta': 'Make an enquiry',
        'paths': [
            ('collab', 'Chefs & restaurants', 'Two kitchens, one dinner.',
             'Once a month we invite a guest chef or restaurant into our kitchen. MOTÍF and Ugruzina have both joined us at HABITS. What would you like to cook together?'),
            ('corporate', 'Company events', 'The whole place for your team.',
             'A team dinner, a client reception or a company party. Book the entire restaurant for your group. Tell us the date you have in mind and how many people are coming.'),
            ('bakery', 'Bakery wholesale', 'Our bakes at your counter.',
             'We supply HABITS pastries to cafés and offices, including our café partner Strange Love in Vilnius. Tell us where you are and how often you would like a delivery.'),
            ('celebration', 'Private celebrations', 'A table for your occasion.',
             'A wedding, a birthday or dinner with the people closest to you. Share your date, guest count and what you have in mind for the evening.'),
        ],
    },
}

def instant_gallery(kind, lang):
    preferred = [photo for photo in GALLERY if kind in photo['kinds']]
    others = [photo for photo in GALLERY if kind not in photo['kinds']]
    title = 'Akimirkos iš HABITS' if lang == 'lt' else 'Moments at HABITS'
    previous = 'Ankstesnės nuotraukos' if lang == 'lt' else 'Previous photos'
    following = 'Kitos nuotraukos' if lang == 'lt' else 'Next photos'
    cards = []
    for photo in preferred + others:
        caption = escape(photo[lang])
        cards.append(f'''<a class="instant-photo" href="{escape(photo['url'])}" target="_blank" rel="noopener noreferrer" aria-label="{caption} · Instagram">
        <figure><img src="/assets/{photo['file']}" loading="lazy" width="{photo['width']}" height="{photo['height']}" alt="{caption}">
        <figcaption><span>{caption}</span><small>Instagram ↗</small></figcaption></figure></a>''')
    return f'''<div class="instant-gallery"><div class="gallery-toolbar"><p>{title}</p><div class="gallery-arrows">
        <button type="button" class="gallery-arrow" data-gallery-step="-1" aria-controls="wall-{kind}" aria-label="{previous}">←</button>
        <button type="button" class="gallery-arrow" data-gallery-step="1" aria-controls="wall-{kind}" aria-label="{following}">→</button>
        </div></div><div class="instant-wall" id="wall-{kind}" role="region" tabindex="0" aria-label="{title}">{''.join(cards)}</div></div>'''


def experiences(lang, picture, labels):
    copy = CONTENT[lang]
    nav = ''.join(f'<button type="button" role="tab" id="tab-{key}" aria-controls="path-{key}" aria-selected="false" data-path="{key}">{label}</button>' for key,label,*_ in copy['paths'])
    panels = []
    for key, label, title, description in copy['paths']:
        panels.append(f'''<article class="path-panel" role="tabpanel" aria-labelledby="tab-{key}" id="path-{key}"><div class="path-description"><h3>{title}</h3><p>{description}</p>
        <a class="button primary" data-inquiry-kind="{key}" href="#inquiry">{copy['cta']} ↗</a></div>{instant_gallery(key, lang)}</article>''')
    return f'''<section id="together" class="together"><header class="archive-heading">{picture('evening',labels['altEvening'])}<div><p class="eyebrow">{copy['label']}</p><h2>{copy['title']}</h2></div></header>
    <div class="path-nav" role="tablist" aria-label="{copy['categories']}">{nav}</div>{''.join(panels)}</section>'''
