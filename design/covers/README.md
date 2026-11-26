# Project cover originals

The rules every cover follows (canvas, safe zone, style, motion tokens, hover,
performance) are in [SPEC.md](SPEC.md).

Source artwork for the animated project covers on the home page, kept as exported so
changes can be requested against a known file. The covers on the site are inline SVGs
in `index.html`; their animation styles live in `assets/css/covers/`.

What the site adds on top of these files: IDs renamed with a per-cover prefix (so they
can't clash on the page), class names on the animated parts, wrapper groups, and
`xlink:href` → `href`. Nothing else in the artwork is changed.

Note: GitHub Pages publishes this folder too (it's reachable by URL, not linked).

| Cover | Tile in `index.html` | SVG class / ID prefix | Styles | Original in this folder |
|---|---|---|---|---|
| White label eCommerce App | `#project2` | `.wl` / `wl-` | `wl.css` | `wl/white-label.svg` (drawn for the site, from a reference export); stills `white-label-1-blue.svg`, `-2-pink.svg`, `-3-orange.svg` |
| DesignOps | `#project10` | `.ops` / `ops-` | `ops.css` | `ops/designops.svg` (site export, animated) |
| Pantry Design System | `#project1` | `.pds` / `pds-` | `pds.css` | `pds/pantry.svg` (drawn for the site, from a screenshot) |
| Data tool | `#project15` | `.xl` / `xl-` | `xl.css` | `xl/data-tool.svg` (drawn for the site, from an Excel-style reference); stills `data-tool-1-spreadsheet.svg`, `data-tool-2-dashboard.svg` |
| Home energy app | `#project16` (link still `#`) | `.nrg` / `nrg-` | `nrg.css` | `nrg/home-energy.svg` (drawn for the site, from a PNG mock-up) |
| AH Compact | `#project4` | `.ah` / `ah-` | `ah.css` | `ah/ah-compact.svg` (site export, animated); originals `ah/groceries.svg`, `ah/iphone-12-mini.svg` |
| Not the brief | `#project13` (currently commented out) | `.ntb` / `ntb-` | `ntb.css` | — Built from `not the brief.svg`, not stored yet |
| Cookbook.md | `#project14` | `.cbk` / `cbk-` | `cbk.css` | `cbk/cookbook.svg` (drawn for the site, including the flat tarte tatin) |
| Island Slide Puzzle | `#project5` | `.isl` / `isl-` | `isl.css` | `isl/island.svg` (site export, animated) |
| Digital Sketching | `.portfolio-wrap.craft` | — | `custom.css` | — Photo (`assets/img/portfolio/portfolio-7.jpg`) |
| Handmade wooden lamp | `#project9` | — | `custom.css` | — Photos (`portfolio-9-day.jpg`, `portfolio-9-night.jpg`) |

## Notes per original

- `ah/ah-compact.svg` is the cover as it is on the site, exported from `index.html` with
  `base.css` and `ah.css` embedded; re-export it after changing the cover. The phone
  screen (shopping UI, free-delivery story) and the order/delivery cycle are drawn for
  the site, after the app's search results list. Six items from `ah/groceries.svg`
  (carrot, juice, baguette, cheese, and the zucchini and tomato over the phone's bottom
  corners) sit in front, each moved toward the sides; `ah/iphone-12-mini.svg` is no
  longer used.
- `isl/island.svg` is no longer the raw Figma export: it is the cover as it is on the
  site, exported from `index.html` with `isl.css` embedded, so it animates when opened in
  a browser (hover the "8" block to slide it). Compared with the original artwork, the
  "8" block sits fully on its front grid slot (`translate(64.6 37.7)` on `.eight-wrap`).
  The animated parts: the two lighthouse beams (`.beam-l`, `.beam-r`), the lamp
  (`.lamp`), the sun halo (`.sun-halo`), the "8" block (`.eight-wrap > .eight`), the
  small water waves (`.wave`, added for the site) and the foam (`.foam`, also copied around the "8" block; its wavy edge
  morphs with SMIL).
  Re-export it after changing the cover. The Figma original is in git history
  (commit 8727804).
- The two `ah/` files are content-identical to the Figma exports; some gradient
  definitions were re-wrapped onto fewer lines. A fresh export can replace them.

## Covers drawn for the site

`wl/`, `pds/`, `xl/`, `nrg/` and `cbk/` hold covers that were drawn in code, so the version on
the site *is* the original. Each file is that inline SVG exported from `index.html` as a
standalone SVG, with its cover's stylesheet (and `base.css`, for the shared motion tokens) embedded: open it in a browser and it
animates as on the site. Edits should go to `index.html` and `assets/css/covers/`, then
be re-exported here. Note that design tools such as Figma ignore the embedded CSS, so on
import some parts show in their pre-animation state (for example the Cookbook editor's
cover boxes and the Data tool's hidden spreadsheet layers).

## Exporting

All exports come from `index.html` through one script:

```
python3 design/covers/export.py            # animated exports, one per cover
python3 design/covers/export.py --stills   # also the stills (needs Google Chrome)
```

- **Animated** (`<folder>/<name>.svg`): the cover's inline SVG with `base.css` and its own
  stylesheet embedded; open it in a browser to see it animate.
- **Stills** (`<name>-1-….svg`, `<name>-2-….svg`, …): for covers whose story has distinct
  stages (Data tool: spreadsheet, dashboard; White label: one per brand). Headless
  Chrome freezes the animation at a moment of the loop and writes the values inline, so
  each file shows one stage. Moments are set in `STILLS` at the top of the script.

Re-run the script after any change to a cover.

## Adding an original

Export from Figma as SVG and save it here under the cover's prefix folder (for example
`ops/designops.svg`), then update the table.
