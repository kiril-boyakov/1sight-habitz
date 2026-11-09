# HABITS Vilnius

Bilingual restaurant landing page, photographed dine-in menu, event gallery and enquiries.

```sh
python3 build.py
python3 verify_site.py
node demo.mjs
```

Open http://127.0.0.1:8765/ for Lithuanian or /en/ for English. The demo server requires Node 22.13 or newer. It stores enquiries locally. See [enquiry setup](INQUIRIES.md) to connect production storage and email.

The menu is maintained in `src/menu.json`. Prices are restaurant prices in euros. The weekday lunch selection and Monday–Thursday differences follow the supplied menu sheets. Pages are generated in `dist/`. Set `HABITS_SITE_ORIGIN` when generating for a different origin.

The demo uses the original HABITS photography, wordmark and fonts. Public event photos link back to the venue’s Breezit gallery and the Sardinele collaboration. Partner stories and translations are maintained in `experiences.py`.

Build the current standalone v7 preview with `python3 preview/build_preview.py`. Menu photo sources are documented in [MEDIA.md](MEDIA.md). Dinner is a separate collaboration format; its individual event menu is announced by HABITS.
