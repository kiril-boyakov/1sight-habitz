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
            f'<div class="category-photo">{picture(image, alt)}</div>'
        )
        if note:
            html.append(f'<p class="category-note">{escape(note)}</p>')
        html.append('</div><div class="category-dishes">')
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
