# HABITS Vilnius website proposal

A complete static, bilingual hospitality website. Lithuanian is the default. All content is pre-rendered HTML, with small progressive enhancements in vanilla JavaScript. There are no application dependencies or installation step.

## Run

From this folder:

```sh
python3 build.py
python3 verify_site.py
python3 -m http.server 8765 --directory dist
```

Open `http://localhost:8765/`. Serve over HTTP; opening `index.html` directly with `file://` does not resolve absolute asset and route paths.

## Routes

| Lithuanian | English | Purpose |
|---|---|---|
| `/` | `/en/` | Homepage, place, evening story and visit details |
| `/menu/` | `/en/menu/` | Six categories and 37 dishes/drinks |
| `/privacy/` | `/en/privacy/` | Actual proposal technology and external services |

Category and dish anchors work directly. Language switching preserves both the route and current URL fragment. Native browser history retains normal back navigation.

## Updating

- `src/content.json`: all page translations and image alt text.
- `src/images.json`: original photo dimensions and responsive WebP variants.
- `src/menu.json`: Vilnius menu data, English translations, delivery-reference prices and provenance.
- `src/site.css`: responsive layout and reduced-motion rules.
- `src/site.js`: modal navigation, focus management, category navigation and photographic reveals.
- `build.py`: semantic pages, metadata, Restaurant JSON-LD and static output.
- `dist/assets/`: placeholder artwork and self-hosted fonts.
- `licenses/`: OFL font licenses for Bricolage Grotesque, Manrope and the Sigmar accent face.

Build again after changing source. To deploy to Netlify, use `python3 build.py` as the build command and `dist` as the publish directory. Set `HABITS_SITE_ORIGIN` to the deployed origin to update metadata.

## Public collaboration copy

The photos, video and original wordmark from the private proposal have been replaced by placeholder artwork and a typeset name. To add approved photographs, put the WebP files in `dist/assets/` and update the variants in `src/images.json` before rebuilding. The menu labels its Wolt delivery reference prices. Confirm dine-in prices, service details and permission to use brand media before a restaurant launch.

Revision 4 adds native-scroll photographic transitions and the revised bilingual menu. Menu search runs locally in the browser and matches names/ingredients without requiring diacritics. No dependency install or new media is needed. All menu entries remain available in the generated HTML when JavaScript is disabled.
