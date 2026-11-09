#!/usr/bin/env python3
"""Build the dependency-free, bilingual HABITS proposal from structured sources."""
from pathlib import Path
from html import escape as esc
import json, os, shutil
from experiences import experiences
from inquiries import inquiry_form

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'dist'
COPY=json.loads((ROOT/'src/content.json').read_text())
from menu_sections import menu_sections
MENU=json.loads((ROOT/'src/menu.json').read_text())
IMAGES=json.loads((ROOT/'src/images.json').read_text())
ORIGIN = os.environ.get('HABITS_SITE_ORIGIN', 'http://localhost:8765').rstrip('/')
IG='https://www.instagram.com/habits.vilnius/'
MAP='https://maps.app.goo.gl/QeZG1PAV4zGpDHnN6'

def arrow(): return ''
def picture(name,alt,classes='',priority=False):
    meta = IMAGES[name]
    variants = [v for v in meta['variants'] if (OUT / 'assets' / v['file']).is_file()]
    if not variants:
        raise FileNotFoundError(f'Missing photographs for {name}')
    chosen = next((v for v in reversed(variants) if v['width'] <= 1600), variants[-1])
    srcset=', '.join('/assets/'+v['file']+' '+str(v['width'])+'w' for v in variants)
    sizes='100vw' if priority or name in ['evening','terrace'] else '(max-width:600px) 100vw, 60vw'
    return f'<picture class="{classes}"><img src="/assets/{chosen["file"]}" srcset="{srcset}" sizes="{sizes}" alt="{esc(alt)}" width="{meta["width"]}" height="{meta["height"]}" {"fetchpriority=high" if priority else "loading=lazy"} decoding="async"></picture>'

def generate(lang,route):
    t=COPY[lang]; base='/' if lang=='lt' else '/en/'
    path=base+(route+'/' if route else '')
    other=('/en/' if lang=='lt' else '/')+(route+'/' if route else '')
    menu=base+'menu/'; booking='https://habits.tablein.com/'+lang
    def external(url,text,cls='text-link'): return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(text)}{arrow()}</a>'
    def button(url,text,cls='primary'):return f'<a class="button {cls}" href="{esc(url)}">{esc(text)}{arrow()}</a>'
    def brand():return f'<a class="brand" href="{base}" aria-label="{t["home"]}"><img src="/assets/wordmark.png" width="686" height="151" alt="HABITS"></a>'
    def languages():
        return '<div class="languages" aria-label="'+('Kalba' if lang=='lt' else 'Language')+'">'+''.join(f'<a href="{path if l==lang else other}" lang="{l}" hreflang="{l}" '+('aria-current="true"' if l==lang else f'data-language="{other}"')+'>'+l.upper()+'</a>'+('<span aria-hidden="true">/</span>' if l=='lt' else '') for l in ['lt','en'])+'</div>'
    def navigation():return f'<a href="{menu}">{t["menu"]}</a><a href="{base}#place">{t["place"]}</a><a href="{base}#together">{t["eventsNav"]}</a><a href="{base}#visit">{t["visit"]}</a>'+external(booking,t['book'],'button primary')
    header=f'''<a class="skip" href="#main">{t['skip']}</a><header class="site-header{' home-header' if not route else ''}">{brand()}<nav class="desktop-nav" aria-label="{'Pagrindinė navigacija' if lang=='lt' else 'Main navigation'}">{navigation()}</nav>{languages()}<button class="menu-toggle" aria-label="{t['navigation']}" aria-controls="mobile-navigation" aria-expanded="false"><i></i><i></i></button></header>
    <dialog class="mobile-dialog" id="mobile-navigation" aria-label="{t['navigation']}"><div class="dialog-head">{brand()}<button class="close-nav">{t['close']} <span aria-hidden="true">×</span></button></div><nav>{navigation()}</nav>{languages()}<p class="dialog-address">Aukštaičių g. 7, Vilnius<br><a href="tel:+37062293186">+370 622 93186</a></p></dialog><noscript><nav class="no-script">{navigation()}</nav></noscript>'''
    footer=f'''<footer class="site-footer">{brand()}<div class="footer-links"><a href="{menu}">{t['menu']}</a><a href="{base}#place">{t['place']}</a><a href="{base}#visit">{t['visit']}</a><a class="social-button" href="{IG}" target="_blank" rel="noopener noreferrer" aria-label="HABITS Instagram"><svg viewBox="0 0 24 24" width="23" height="23" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3.4" y="3.4" width="17.2" height="17.2" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.6" r=".9" fill="currentColor" stroke="none"/></svg></a><a href="{base}privacy/">{t['privacy']}</a></div><div class="footer-bottom"><span>HABITS · Vilnius</span></div></footer><nav class="mobile-actions{' hidden' if not route else ''}" aria-label="{'Greitos nuorodos' if lang=='lt' else 'Quick actions'}"><a href="{menu}">{t['menu']}</a>{external(booking,t['book'],'')}</nav>'''
    if not route:
        body=f'''<main id="main"><section class="hero" aria-labelledby="hero-title">{picture('hero',t['altHero'],'hero-poster',priority=True)}<video class="hero-film" autoplay data-src="/assets/habits-film.mp4" muted playsinline loop preload="metadata" aria-hidden="true" poster="/assets/hero-1080.webp"></video><div class="hero-content"><p class="eyebrow">{t['heroLabel']}</p><h1 id="hero-title"><span>{t['hero1']}</span> <span>{t['hero2']}</span></h1><p class="hero-copy">{t['heroCopy']}</p><div class="hero-actions">{button(menu,t['explore'],'light')}{external(booking,t['book'],'button ghost')}</div></div></section>
        <section class="intro" id="place"><div class="intro-copy reveal"><p class="eyebrow">{t['introLabel']}</p><h2>{t['introTitle'].replace('Geri įpročiai', '<span class=brand-phrase>Geri įpročiai</span>').replace('Good habits', '<span class=brand-phrase>Good habits</span>')}</h2><p>{t['introCopy']}</p><a class="text-link" href="#visit">{t['placeLink']}{arrow()}</a></div><div class="intro-visual"><div class="intro-photo scene-large drift-frame" data-drift="28">{picture('venue',t['altVenue'])}</div><figure class="coffee-detail reveal">{picture('coffee',t['altCoffee'])}<figcaption>{t['coffeeDetail']}</figcaption></figure></div></section>
        <section class="table-moment" data-scroll-scene aria-label="{t['sceneCopy']}">{picture('terrace',t['altTerrace'])}<h2>{''.join('<span>'+esc(part.strip())+'.</span>' for part in t['sceneCopy'].split('.') if part.strip())}</h2></section>
        <section class="menu-preview"><div class="section-top"><div><p class="eyebrow">{t['foodLabel']}</p><h2>{t['foodTitle']}</h2></div><a class="text-link" href="{menu}">{t['fullMenu']}{arrow()}</a></div><div class="food-editorial"><div class="food-photo scene-large drift-frame" data-drift="22">{picture('sandwich',t['altSandwich'])}</div><div class="highlight-list">'''
        for i,target in enumerate(['dish-sandwiches-0','dish-breakfast-6','lunch'],1):
            body+=f'<a class="highlight reveal" href="{menu}#{target}"><h3>{t[f"highlight{i}"]}{arrow()}</h3><p>{t[f"highlight{i}Copy"]}</p></a>'
        body+=f'''</div></div></section>{experiences(lang,picture,t)}{inquiry_form(lang)}
        <section class="visit" id="visit"><div><p class="eyebrow">{t['visitLabel']}</p><h2>{t['visitTitle']}</h2><div class="visit-map"><a class="map-preview" href="{MAP}" target="_blank" rel="noopener noreferrer" aria-label="{t['directions']} · HABITS"><img src="/assets/location-map.svg" width="720" height="400" alt="HABITS · Paupys · Vilnius"><span class="map-open">{t['directions']} ↗</span></a><a href="{MAP}" target="_blank" rel="noopener noreferrer"><span>{t['address']}</span><span>Google Maps ↗</span></a></div></div><div class="visit-details reveal"><h3>{t['visitSub']}</h3><dl><div class="visit-row"><dt>{t['addressLabel']}</dt><dd>{t['address']}<br>{external(MAP,t['directions'])}</dd></div><div class="visit-row"><dt>{t['phoneLabel']}</dt><dd><a href="tel:+37062293186">+370 622 93186</a></dd></div><div class="visit-row"><dt>{t['hoursLabel']}</dt><dd>{t['hours']}</dd></div></dl><div class="visit-actions">{external(booking,t['book'],'button primary')}{button('tel:+37062293186',t['call'],'')}</div><p class="visit-note">{t['bookingNote']}</p></div></section></main>'''
    elif route=='menu':
        body=f'''<main id="main" class="menu-page"><section class="menu-heading"><div class="menu-heading-copy"><p class="eyebrow">BRUNCH · HABITS VILNIUS</p><h1>{t['menuHeading']}</h1><p>{t['menuIntro']}</p></div><div class="menu-cover" aria-label="{t['menuAsideLabel']}"><div class="menu-cover-main">{picture('sandwich',t['altSandwich'],priority=True)}</div><div class="menu-cover-round">{picture('table',t['altTable'])}</div><p class="menu-cover-note">{t['menuCoverNote']}</p></div></section><nav class="category-nav" aria-label="{t['categoryLabel']}"><div class="category-links">'''
        for cat in MENU['categories']:body+=f'<a href="#{cat["id"]}">{cat[lang]}</a>'
        body+=f'''</div><div class="menu-search" hidden><label class="sr-only" for="dish-search">{t['searchLabel']}</label><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg><input id="dish-search" type="search" placeholder="{t['searchLabel']}" autocomplete="off"><button type="button" class="clear-search" aria-label="{t['clearSearch']}" hidden>×</button></div></nav><div class="menu-results" role="status" aria-live="polite" data-empty="{t['noResults']}" data-count="{t['resultsCount']}"></div><div class="menu-layout"><div class="menu-list">'''
        body+=menu_sections(MENU, lang, t, picture)
        body+=f'''</div></div><div class="menu-end"><p class="allergy-note">{t['allergy']} <a href="tel:+37062293186">+370 622 93186</a>{t['allergyEnd']}</p><div><p class="eyebrow">{t['menuAsideLabel']}</p><h2>{t['menuAside']}</h2>{external(booking,t['book'],'button primary')}</div></div></main>'''
    else:
        body=f'''<main id="main" class="privacy-page"><h1>{t['privacyTitle']}</h1><p>{t['privacyIntro']}</p><h2>{t['privacyExternal']}</h2><p>{t['privacyExternalCopy']}</p><p><a href="https://www.tablein.com/privacy" target="_blank" rel="noopener noreferrer">Tablein — {t['privacy']}</a></p><h2>{t['privacyHosting']}</h2><p>{t['privacyHostingCopy']}</p></main>'''
    title=t['menuTitle'] if route=='menu' else ('HABITS Vilnius — '+t['privacy'] if route else t['title'])
    description=t['menuDescription'] if route=='menu' else t['description']
    ltpath='/' +(route+'/' if route else '');enpath='/en/'+(route+'/' if route else '')
    schema={'@context':'https://schema.org','@type':'Restaurant','name':'HABITS','telephone':'+37062293186','address':{'@type':'PostalAddress','streetAddress':'Aukštaičių g. 7','addressLocality':'Vilnius','addressCountry':'LT'},'sameAs':[IG],'url':ORIGIN+base,'hasMenu':ORIGIN+menu,'acceptsReservations':booking}
    head=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><meta name="color-scheme" content="light"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#f3f0e9"><link rel="canonical" href="{ORIGIN+path}"><link rel="alternate" hreflang="lt" href="{ORIGIN+ltpath}"><link rel="alternate" hreflang="en" href="{ORIGIN+enpath}"><link rel="alternate" hreflang="x-default" href="{ORIGIN+ltpath}"><meta property="og:type" content="website"><meta property="og:site_name" content="HABITS Vilnius"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{ORIGIN+path}"><meta property="og:locale" content="{'lt_LT' if lang=='lt' else 'en_GB'}"><meta property="og:locale:alternate" content="{'en_GB' if lang=='lt' else 'lt_LT'}"><meta property="og:image" content="{ORIGIN}/assets/social.jpg"><meta property="og:image:alt" content="HABITS Vilnius"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/assets/favicon.png"><link rel="stylesheet" href="/assets/site.css?v=8"><link rel="stylesheet" href="/assets/inquiry.css?v=8"><script src="/assets/site.js?v=8" defer></script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body>'''
    dest=OUT/(path.lstrip('/'))/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(head+header+body+footer+'</body></html>')

OUT.mkdir(exist_ok=True)
(OUT / 'assets').mkdir(exist_ok=True)
for lang in COPY:
    for route in ['','menu','privacy']:generate(lang,route)
for filename in ['site.css','site.js','inquiry.js','inquiry.css','location-map.svg']:shutil.copy(ROOT/'src'/filename,OUT/'assets'/filename)
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Robots-Tag: noindex, nofollow\n/assets/*\n  Cache-Control: public, max-age=86400\n')
(OUT/'404.html').write_text('<!doctype html><html lang="lt"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>HABITS — 404</title><style>body{background:#f3f0e9;color:#282923;font:20px system-ui;padding:10vw}a{color:inherit}</style><h1>HABITS</h1><p>Puslapio neradome. / Page not found.</p><a href="/">Pradžia / Home</a></html>')
print('Built six localized pages.')
