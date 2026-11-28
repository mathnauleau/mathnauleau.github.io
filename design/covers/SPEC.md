# Project cover spec

Rules for the animated covers on the home page, so they read as one set. Every new
cover follows them; existing covers are brought in line using the table at the end.
Values marked `--cover-…` live in `assets/css/covers/base.css`.

## 1. Canvas

- Inline `<svg viewBox="0 0 800 500">` inside `.portfolio-wrap`, with `role="img"` and an
  `aria-label` naming the project.
- One prefix per cover (`.xl`, `xl-…` IDs, `xl.css`); every rule inside `@scope (.<prefix>)`.
- **Safe zone.** On the tall tiles (4:3) the drawing fades out from **y = 370** (a mask from
  74% to 100% of its height) and the title starts at y ≈ 424–497 depending on the width
  (measured at 1024–1600px). Keep everything that carries meaning **above y = 370**, and
  **40 units** in from the left and right edges. Below 370 is for background, the bottom
  of a device, or secondary detail that may fade.

## 2. Composition and style

- **One hero element** per cover: the thing the eye lands on and the thing that responds to
  hover.
- **Client work** (Design section) is drawn as **flat UI**: real layouts, skeleton bars for
  copy, no photos, no illustrated objects. **Side projects** (Craft section) may be
  illustrated.
- Never mix rendering styles inside one cover (for example a realistic device with flat
  illustrations, or a photo inside flat UI).
- **Device frames** are shared, never redrawn:
  - **Window:** 660 × 400 at (70, 55), radius 20, title bar with three dots (Data tool,
    Pantry).
  - **Phone:** 300 × 590 at `translate(248 40)`; frame and side buttons white at 40%,
    bezel `#2B2E35` (288 × 578, radius 52, inset 6), screen 276 wide, radius 48, inset 12;
    island 88 × 28 at (106, 30); no status bar (Home energy app, AH Compact).
  - **No drop shadows** on device frames: they sit flat on the background.

## 3. Colour

- One background hue per tile: a gradient at 32° on the tile, and continuing the drawing's
  bottom edge under the title on tall tiles.
- **Neighbouring tiles never share a hue family.** Current hues: DesignOps coral, Data tool
  green, Pantry blue-violet, Home energy gold-to-purple, White label navy-teal, AH blue.
- Title and description on the tile are white, and must reach 4.5:1 against the bottom of
  the drawing.

## 4. Text inside a cover

- Text meant to be read is at least **14 units** in the 800-wide drawing (about 11px in the
  desktop grid). Smaller than that, use skeleton bars instead of words.
- UI text in Inter. Use a brand typeface only when the story is about type (White label).
- No copy that repeats the tile's own title.

## 5. Motion

| Token | Value | Use |
|---|---|---|
| `--cover-story` | 12s | A cover that tells its project's story, in beats of about 3s |
| `--cover-ambient` | 7s | Background life: floats, drifts, glows |
| `--cover-ease` | `cubic-bezier(0.4, 0, 0.2, 1)` | Default easing for everything |
| `--cover-ease-pop` | `cubic-bezier(0.3, 0.8, 0.3, 1.1)` | At most **one** small "pop" per cover |
| `--cover-ambient-amplitude` | 8px | Largest ambient movement |

- A cover has **one story loop** (12s) **or** only ambient motion, plus ambient life if
  needed. All parts of a story share the one loop (no separate timers drifting apart).
- Ambient motion stays at or under 8 units and is out of step between elements.
- **Travel along a path** (a light running along a line, a dot along a connection) is
  not limited to 8 units; its loop is a whole multiple of `--cover-ambient`, with starts
  spaced evenly (DesignOps: 4 × 7s, starts 7s apart; Home energy app: 7s).
- No springy overshoot except the single `--cover-ease-pop`.
- **Reduced motion:** every CSS animation stops (`animation: none`), and the cover shows its
  **finished state** (the end of the story), never a blank or half-drawn one. SMIL
  animations are paused by `js/covers.js`; elements that only make sense moving (travelling
  dots, notifications) are hidden.

## 6. Hover

- Real pointer and wide screen only: `@media (hover: hover) and (min-width: 769px)`.
- The **hero element lifts** by `--cover-hover-lift` (6px) over `--cover-hover-duration`
  (300ms) with `--cover-ease`. Nothing else moves.
- Exception: a hover that explains the product, using the same duration and easing
  (Island: the block slides toward the gap; DesignOps: the "O" toggle switches on).

## 7. Performance

- `js/covers.js` pauses every cover that is off screen (CSS and SMIL) and resumes it when
  it scrolls back in. New covers need nothing extra, as long as they sit in
  `.portfolio-wrap > svg`.
- No blur filters or `mix-blend-mode` on elements that animate.
- Inline SVG budget: about 30 KB per cover. Larger artwork (Island, AH groceries) should be
  simplified or moved to an external file.

## 8. Export

Each cover has a standalone copy in `design/covers/<prefix>/` with its stylesheet embedded
(see the README). Re-export after every change.

## Where the covers stand today

✅ meets the spec · ⚠️ partly · ❌ not yet

| Cover | Loop | Easing | Hover | Safe zone | Style | Text ≥ 14 | Notes |
|---|---|---|---|---|---|---|---|
| DesignOps | ✅ ambient + travel (4 × 7s) | ✅ | ✅ toggle (exception) | ✅ | ✅ | ✅ | Wordmark repeats the tile title |
| Data tool | ✅ 12s | ✅ one pop | ✅ window lifts 6px | ✅ | ✅ | ⚠️ | |
| Pantry | ✅ 7s ambient, staggered | ✅ | ✅ cards lift 6px | ✅ (card labels start to fade) | ✅ | ❌ nav text | Caret blinks at 1s (UI convention) |
| Home energy app | ✅ 12s (+ 7s travel) | ✅ | ❌ none | ⚠️ bottom labels and stat tiles fade | ✅ | ❌ 11-unit labels | |
| White label | ✅ 12s (+ 7s ambient) | ⚠️ knob and lift overshoot | ⚠️ lifts 12px, every screen | ✅ | ✅ | ⚠️ | |
| AH Compact | ✅ 12s story + 7s ambient | ✅ one pop | ✅ groceries lift 6px | ✅ | ⚠️ flat UI phone with illustrated groceries in front | ✅ | Product cards to follow a reference layout |
| Cookbook.md | ❌ 16s | ⚠️ card lift overshoot | ✅ lifts 6px | ✅ | ✅ flat tart | ✅ | |
| Island | ✅ ambient only | ✅ | ✅ exception | ✅ | ✅ | — | 88 KB; foam is SMIL (paused by covers.js under reduced motion) |
