# AR&SMART website — notes for whoever edits it next

Static site on GitHub Pages (branch `main`, domain in `CNAME`). No build server: you edit files, commit and push, and the site goes live a minute later.

## Where things live
- `index.html` — the whole store as one RTL hash-routed page: `#home`, `#c-<cat>`, `#b-<brand>`, `#p-<id>`, `#search`, `#works`, `#offers-all`…
  - Inline arrays in the `<script>`: `PRODUCTS` (cameras, recorders, intercom, network…), `CATS`, `BRANDS`, `OFFERS`, `WORKS` (portfolio), `WK` (portfolio filters).
- `catalog.js` — `window.TYPES` and `window.CATALOG` (locks, access control, smart home, sound, PBX). When you change it, bump `catalog.js?v=N` in `index.html`.
- Product fields: `id, img, imgs (gallery), cat, t (type), b (brand), n (Arabic name), m (model), c (supplier code), p (price EGP; 0 = out of stock), s (spec bullets), d, h`.
- Images:
  - Products: `img/p/<id>.jpg`, 600×600 on white. Gallery images are `img/p/<id>-1.jpg`…
  - Portfolio: `img/w/<name>.jpg` (about 1400 px), with a thumbnail of about 640 px in `img/w/t/`.
  - Offers: `img/off/`.
- Static SEO pages: `p/*.html`, `services/*.html`, `areas/*.html` and `sitemap.xml` are GENERATED. Rebuild them after any product change:
  ```
  npm i playwright   # once, anywhere on NODE_PATH (Chromium must be available)
  node _tools/export.js && python3 _tools/build_pages.py
  ```

## Checks before every push
- Load the page with Playwright at 390 px and 1280 px wide:
  - no `pageerror`
  - no broken images
  - `scrollWidth - innerWidth == 0` (no sideways scroll)
- Open the changed product: `index.html#p-<id>` and `p/<id>.html`.
- Before committing, run `git pull`. After pushing, check that `git ls-remote origin main` matches the commit you just made.

## Pricing conventions
- Prices the owner sends directly (screenshots, chat) are used exactly as given.
- Supplier-catalog prices got +15%, rounded up:
  - under 100 → to the nearest 1
  - under 1000 → to the nearest 5
  - under 10000 → to the nearest 10
  - else → to the nearest 50
- EXCEPTION (owner, 31-10-2026): SIB catalog items (ids `sib-*`, `sibl-*`, `zoom-*`) must be the catalog price exactly, no +15%. Not applied yet.
- Never show wholesale/cost prices on the site.

## Photos
Blur faces and car plates in portfolio photos, except the owner's own face.
