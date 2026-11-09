"""Bilingual enquiry form shared by both landing pages."""
from html import escape

LABELS = {
    'lt': {
        'heading': 'Parašykite mums', 'kind': 'Dėl ko kreipiatės?',
        'types': ('Bendradarbiavimas su šefais ir restoranais', 'Restorano nuoma įmonei', 'Kepinių tiekimas', 'Asmeninė šventė'),
        'name': 'Vardas', 'email': 'El. paštas', 'message': 'Jūsų sumanymas',
        'hints': ('Kokį bendrą vakarą norėtumėte surengti?', 'Kada planuojate renginį ir kiek žmonių dalyvaus?', 'Kur ir kaip dažnai norėtumėte gauti kepinių?', 'Ką švęsite, kada ir kiek svečių laukiate?'),
        'send': 'Siųsti užklausą', 'sending': 'Siunčiama…',
        'success': 'Užklausą gavome. Atsakysime jūsų nurodytu el. paštu.',
        'demo': 'Užklausa išsaugota šioje demonstracinėje versijoje.',
        'error': 'Užklausos išsiųsti nepavyko. Bandykite dar kartą arba parašykite el. paštu.',
        'privacy': 'Kaip tvarkome jūsų duomenis', 'direct': 'Taip pat galite parašyti tiesiogiai',
        'choose': 'Pasirinkite temą', 'nojs': 'Norėdami pateikti užklausą, parašykite mums el. paštu.',
    },
    'en': {
        'heading': 'Get in touch', 'kind': 'What are you planning?',
        'types': ('Chef or restaurant collaboration', 'Private hire for a company', 'Bakery deliveries', 'Personal celebration'),
        'name': 'Your name', 'email': 'Email', 'message': 'Tell us about it',
        'hints': ('What would you like to create together?', 'When is your event and how many people will attend?', 'Where and how often would you like deliveries?', 'What are you celebrating, when and with how many guests?'),
        'send': 'Send enquiry', 'sending': 'Sending…',
        'success': 'We received your enquiry. We’ll reply to the email address you gave us.',
        'demo': 'Your enquiry was saved in this demo.',
        'error': 'We couldn’t send your enquiry. Try again or email us directly.',
        'privacy': 'How we use your details', 'direct': 'You can also email us directly',
        'choose': 'Select a topic', 'nojs': 'To make an enquiry, please email us directly.',
    },
}
KINDS = ('collab', 'corporate', 'bakery', 'celebration')


def inquiry_form(lang):
    t = LABELS[lang]
    options = ''.join(
        f'<option value="{kind}" data-hint="{escape(hint, quote=True)}">{label}</option>'
        for kind, label, hint in zip(KINDS, t['types'], t['hints'])
    )
    privacy = '/privacy/' if lang == 'lt' else '/en/privacy/'
    return f'''<section class="contact-inquiry" id="inquiry" aria-labelledby="inquiry-title">
    <div class="inquiry-intro"><h2 id="inquiry-title">{t["heading"]}</h2>
    <p>{t["direct"]}<br><a class="text-link" href="mailto:manager@habits.lt">manager@habits.lt</a></p></div>
    <form id="inquiry-form" action="/api/inquiries" method="post" hidden data-sending="{t["sending"]}" data-success="{t["success"]}" data-demo="{t["demo"]}" data-error="{t["error"]}">
    <label class="inquiry-wide">{t["kind"]}<select name="kind" id="inquiry-kind" required>
    <option value="">{t["choose"]}</option>{options}</select></label>
    <label>{t["name"]}<input name="name" autocomplete="name" maxlength="120" required></label>
    <label>{t["email"]}<input name="email" type="email" autocomplete="email" maxlength="254" required></label>
    <label class="inquiry-wide">{t["message"]}<textarea name="message" rows="3" maxlength="3000" required></textarea></label>
    <div class="inquiry-wide inquiry-send"><button class="button primary" type="submit">{t["send"]}</button>
    <a href="{privacy}">{t["privacy"]}</a></div>
    <p class="inquiry-wide inquiry-status" role="status" aria-live="polite"></p></form>
    <noscript><p>{t["nojs"]}</p></noscript></section>
    <script src="/assets/inquiry.js" defer></script>'''
