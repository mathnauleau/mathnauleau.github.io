# Project cover originals

Source artwork for the animated project covers on the home page, kept as exported so
changes can be requested against a known file. The covers on the site are inline SVGs
in `index.html`; their animation styles live in `assets/css/covers/`.

What the site adds on top of these files: IDs renamed with a per-cover prefix (so they
can't clash on the page), class names on the animated parts, wrapper groups, and
`xlink:href` → `href`. Nothing else in the artwork is changed.

Note: GitHub Pages publishes this folder too (it's reachable by URL, not linked).

| Cover | Tile in `index.html` | SVG class / ID prefix | Styles | Original in this folder |
|---|---|---|---|---|
| White label eCommerce App | `#project2` | `.wl` / `wl-` | `wl.css` | `wl/white-label.svg` (drawn for the site, from a reference export) |
| DesignOps | `#project10` | `.ops` / `ops-` | `ops.css` | — Built from `project-hero-mobile.svg` (DesignOps), not stored yet |
| Pantry Design System | `#project1` | `.pds` / `pds-` | `pds.css` | `pds/pantry.svg` (drawn for the site, from a screenshot) |
| Data tool | `#project15` | `.xl` / `xl-` | `xl.css` | `xl/data-tool.svg` (drawn for the site, from an Excel-style reference) |
| Home energy app | `#project16` (link still `#`) | `.nrg` / `nrg-` | `nrg.css` | `nrg/home-energy.svg` (drawn for the site, from a PNG mock-up) |
| AH Compact | `#project4` | `.ah` / `ah-` | `ah.css` | `ah/ah-compact.svg` (site export, animated); originals `ah/groceries.svg`, `ah/iphone-12-mini.svg` |
| Not the brief | `#project13` (currently commented out) | `.ntb` / `ntb-` | `ntb.css` | — Built from `not the brief.svg`, not stored yet |
| Cookbook.md | `#project14` | `.cbk` / `cbk-` | `cbk.css` | `cbk/cookbook.svg` (drawn for the site; the card photo is `assets/img/portfolio/cookbook-tarte-tatin.jpg`, embedded in the export) |
| Island Slide Puzzle | `#project5` | `.isl` / `isl-` | `isl.css` | `isl/island.svg` (site export, animated) |
| Digital Sketching | `.portfolio-wrap.craft` | — | `custom.css` | — Photo (`assets/img/portfolio/portfolio-7.jpg`) |
| Handmade wooden lamp | `#project9` | — | `custom.css` | — Photos (`portfolio-9-day.jpg`, `portfolio-9-night.jpg`) |

## Notes per original

- `ah/groceries.svg` is placed in the cover at `translate(144 297.5) scale(.963)`; each
  of its nine items (tray, milk, zucchini, carrot, juice, baguette, orange, tomato,
  cheese) is wrapped in its own `.bob` group for the bounce.
- `ah/ah-compact.svg` is the cover as it is on the site, exported from `index.html` with
  `ah.css` embedded; re-export it after changing the cover.
- `ah/iphone-12-mini.svg` is no longer drawn as the phone: the cover now uses the
  titanium phone from the Home energy app cover at exactly the same size and place
  (`translate(248.75 40) scale(1.0083)`). Only its outlined screen copy ("Daily
  groceries / Free delivery") is still used, on a blue screen.
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
standalone SVG, with its cover's stylesheet embedded: open it in a browser and it
animates as on the site. Edits should go to `index.html` and `assets/css/covers/`, then
be re-exported here. Note that design tools such as Figma ignore the embedded CSS, so on
import some parts show in their pre-animation state (for example the Cookbook editor's
cover boxes and the Data tool's hidden spreadsheet layers).

## Adding an original

Export from Figma as SVG and save it here under the cover's prefix folder (for example
`ops/designops.svg`), then update the table.
