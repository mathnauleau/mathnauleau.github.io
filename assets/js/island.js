/* Island Slide Puzzle cover: pointer-follow parallax.
   Layers are the [data-depth] groups inside the inline SVG in #project5. A bigger depth
   means closer, so it travels further (SVG units). One requestAnimationFrame loop eases
   the layers toward the pointer and sleeps once they settle. Off for touch, narrow
   screens and prefers-reduced-motion, same gating as the hover lift in custom.css. */
(function () {
  const stage = document.getElementById('project5');
  const svg = stage && stage.querySelector('.isl');
  if (!svg) return;

  const layers = Array.from(svg.querySelectorAll('[data-depth]')).map((el) => ({
    el,
    k: parseFloat(el.getAttribute('data-depth')) || 0,
  }));
  const allowed = window.matchMedia(
    '(hover: hover) and (min-width: 769px) and (prefers-reduced-motion: no-preference)'
  );
  let tx = 0, ty = 0, x = 0, y = 0, raf = 0;

  function paint() {
    for (const l of layers) {
      l.el.style.transform = 'translate(' + (x * l.k).toFixed(2) + 'px, ' + (y * l.k).toFixed(2) + 'px)';
    }
  }

  function tick() {
    raf = 0;
    x += (tx - x) * 0.1;
    y += (ty - y) * 0.1;
    paint();
    if (Math.abs(tx - x) > 0.001 || Math.abs(ty - y) > 0.001) raf = requestAnimationFrame(tick);
  }

  function kick() {
    if (!raf) raf = requestAnimationFrame(tick);
  }

  function reset() {
    tx = ty = x = y = 0;
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    for (const l of layers) l.el.style.transform = '';
  }

  stage.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse' || !allowed.matches) return;
    const r = stage.getBoundingClientRect();
    tx = ((e.clientX - r.left) / r.width - 0.5) * 2;
    ty = ((e.clientY - r.top) / r.height - 0.5) * 2;
    kick();
  });

  stage.addEventListener('pointerleave', () => {
    tx = ty = 0;
    if (allowed.matches) kick();
  });

  allowed.addEventListener('change', (e) => {
    if (!e.matches) reset();
  });
})();
