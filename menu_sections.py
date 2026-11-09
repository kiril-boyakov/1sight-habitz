"""Render the photographed restaurant menus in either site language."""
from html import escape


def format_price(amounts, lang):
    """Keep printed paired prices in order, without inferring portion sizes."""
    values = amounts if isinstance(amounts, list) else [amounts]
    numbers = [f'{value:g}' for value in values]
    if lang == 'lt':
        return ' / '.join(n.replace('.', ',') for n in numbers) + ' €'
    return '€' + ' / €'.join(numbers)


def menu_sections(menu, lang, copy, picture):
    html = []
    for category in menu['categories']:
        category_id = category['id']
        image = category['image']
        alt = copy['alt' + image.capitalize()]
        note = category['notes'][lang]
        html.append(
            f'<section class="menu-section" id="{category_id}">'
            f'<div class="category-intro"><h2>{escape(category[lang])}</h2>'
        )
        html.append(f'<div class="category-photo">{picture(image, alt)}</div>')
        if category_id == 'lunch':
            html.append(f'<div class="category-photo category-photo-extra">{picture("menu-lunch-main", copy["altMenu-lunch-main"])}</div>')
        if note:
            html.append(f'<p class="category-note">{escape(note)}</p>')
        html.append('</div><div class="category-dishes">')
        if category_id == 'lunch':
            combo = format_price(12, lang)
            html.append(f'<div class="lunch-offer"><div><p class="lunch-days">{copy["lunchDays"]}</p><p class="lunch-hours">11:00–14:00</p></div><div class="lunch-combo"><span>{copy["lunchCombo"]}</span><strong>{combo}</strong></div><p class="lunch-individual">{copy["lunchSoup"]} {format_price(3.5, lang)} <span>·</span> {copy["lunchMain"]} {format_price(11, lang)}</p></div>')
        if category.get('format') == 'collaboration':
            html.append(f'<div class="dinner-invitation"><p class="eyebrow">{copy["dinnerBadge"]}</p><h3>{copy["dinnerTitle"]}</h3><p>{copy["dinnerCopy"]}</p><div class="dinner-actions"><a class="button primary" href="https://www.instagram.com/habits.vilnius/" target="_blank" rel="noopener noreferrer">{copy["dinnerNews"]}</a><a class="text-link" href="mailto:manager@habits.lt">{copy["dinnerEnquiry"]}</a></div></div>')
        index = 0
        for group in category['groups']:
            html.append('<div class="dish-group">')
            if group[lang]:
                html.append(f'<h3 class="dish-group-title">{escape(group[lang])}</h3>')
            html.append('<div class="dish-grid">')
            heading = 'h4' if group[lang] else 'h3'
            for lt, en, desc_lt, desc_en, amounts in group['items']:
                name, description = (lt, desc_lt) if lang == 'lt' else (en, desc_en)
                dish_id = f'dish-{category_id}-{index}'
                price = format_price(amounts, lang)
                html.append(
                    f'<article class="dish" id="{dish_id}"><div class="dish-top">'
                    f'<{heading}><a href="#{dish_id}">{escape(name)}</a></{heading}>'
                    f'<span class="dish-price">{escape(price)}</span></div>'
                )
                if description:
                    html.append(f'<p>{escape(description)}</p>')
                html.append('</article>')
                index += 1
            html.append('</div></div>')
        html.append('</div></section>')
    return ''.join(html)
