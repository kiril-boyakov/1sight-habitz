"""The event archive and four enquiry paths share one place on the homepage."""

GALLERY = 'https://breezit.lt/habits-bakery'
ARCHIVE = 'https://www.findglocal.com/LT/Kaunas/110119375344752/Habits-Bakery'
PHOTOS = 'https://breezit.s3.eu-north-1.amazonaws.com/'
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
        'photos': [('Vestuvės HABITS', 'Jaunavedžiai ir svečiai su šaltosiomis ugnelėmis'), ('Šventės stalas', 'Gėlėmis papuoštas šventės stalas'), ('Vakaras su svečiais', 'Šventės svečiai HABITS restorane')],
        'motif': 'HABITS × MOTÍF', 'motif_note': '2026 05 21 · Antroji bendra vakarienė',
        'ug': 'HABITS × Ugruzina', 'ug_note': 'Svečių virtuvė', 'archive': 'Vakarienės skelbimas',
        'gallery':'Renginių galerija', 'partner':'Mūsų partneris', 'photos_link':'Visa švenčių galerija',
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
        'photos': [('A HABITS wedding', 'Newlyweds and guests holding sparklers'), ('Set for dinner', 'Flowers on a table set for a celebration'), ('An evening at HABITS', 'Party guests inside HABITS')],
        'motif': 'HABITS × MOTÍF', 'motif_note': '21 May 2026 · Our second dinner together',
        'ug': 'HABITS × Ugruzina', 'ug_note': 'Guest kitchen', 'archive': 'Dinner announcement',
        'gallery':'Event gallery', 'partner':'Our partner', 'photos_link':'See the celebration gallery',
    },
}

def experiences(lang, picture, labels):
    copy = CONTENT[lang]
    paths = copy['paths']
    nav = ''.join(f'<a href="#path-{key}" data-path="{key}">{label}</a>' for key,label,*_ in paths)
    panels = []
    for key, label, title, description in paths:
        if key == 'collab':
            visual = f'''<div class="dinner-archive"><div><small>{copy['ug_note']}</small><b>{copy['ug']}</b></div>
                <div><small>{copy['motif_note']}</small><b>{copy['motif']}</b><a class="text-link" href="{ARCHIVE}" target="_blank" rel="noopener">{copy['archive']} ↗</a></div></div>'''
            meal = 'Omega 3 pusryčiai' if lang == 'lt' else 'The Omega 3 breakfast'
            visual = f'''<div class="collab-album"><a class="collab-feature" href="https://sardinele.lt/en/blogs/articles/sardines-for-brunch" target="_blank" rel="noopener">
                <img loading="lazy" src="https://cdn.shopify.com/s/files/1/0643/2394/4606/files/HabitsBakery_and_Sardinele_dish.png?v=1747418273" width="280" height="300" alt="{meal}"><span><small>{meal}</small>HABITS × Sardinele ↗</span></a>{visual}</div>'''
        elif key == 'bakery':
            visual = f'''<figure class="bakery-partner">{picture('pastry',labels['altPastry'])}<figcaption>{copy['partner']} · <a href="https://strangelove.lt/">Strange Love ↗</a></figcaption></figure>'''
        else:
            indices = [1,2] if key=='corporate' else [0,1,2]
            files = ['1790249461552','1790249466086','1790249470646']
            figures = ''.join(f'<figure><a href="{GALLERY}" target="_blank" rel="noopener"><img loading="lazy" width="480" height="540" alt="{alt}" src="{PHOTOS}{files[i]}-thumb-photo.jpg"></a><figcaption>{caption}</figcaption></figure>' for i in indices for caption,alt in [copy['photos'][i]])
            visual = f'<div class="occasion-gallery">{figures}<a class="gallery-source" href="{GALLERY}">{copy["photos_link"]} ↗</a></div>'
        panels.append(f'''<article class="path-panel" id="path-{key}"><div class="path-description"><h3>{title}</h3><p>{description}</p>
        <a class="button primary" data-inquiry-kind="{key}" href="#inquiry">{copy['cta']} ↗</a></div>{visual}</article>''')
    return f'''<section id="together" class="together"><header class="archive-heading">{picture('evening',labels['altEvening'])}<div><p class="eyebrow">{copy['label']}</p><h2>{copy['title']}</h2></div></header>
    <nav class="path-nav" aria-label="{copy['categories']}">{nav}</nav>{''.join(panels)}</section>'''
