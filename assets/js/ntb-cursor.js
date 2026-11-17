/* Not the brief cover: the drawn cursor trails the pointer.
   The cursor is the .ntb-cursor group inside the inline SVG in #project13; its tip sits
   at the group's origin, so it is placed with a translate in SVG units. One
   requestAnimationFrame loop eases it toward the pointer and sleeps once settled.
   On leave it glides back to its resting spot. Off for touch, narrow screens and
   prefers-reduced-motion, same gating as the hover effects in custom.css. */
(function () {
  const stage = document.getElementById('project13');
  const svg = stage && stage.querySelector('.ntb');
  const cursor = svg && svg.querySelector('.ntb-cursor');
  if (!cursor) return;

  const REST_X = 485, REST_Y = 335;
  const VB = svg.viewBox.baseVal;
  const allowed = window.matchMedia(
    '(hover: hover) and (min-width: 769px) and (prefers-reduced-motion: no-preference)'
  );
  let tx = REST_X, ty = REST_Y, x = REST_X, y = REST_Y, raf = 0;

  function paint() {
    cursor.setAttribute('transform', 'translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')');
  }

  function tick() {
    raf = 0;
    x += (tx - x) * 0.18;
    y += (ty - y) * 0.18;
    if (Math.abs(tx - x) < 0.05 && Math.abs(ty - y) < 0.05) { x = tx; y = ty; }
    paint();
    if (x !== tx || y !== ty) raf = requestAnimationFrame(tick);
  }

  function kick() {
    if (!raf) raf = requestAnimationFrame(tick);
  }

  function reset() {
    tx = x = REST_X;
    ty = y = REST_Y;
    if (raf) { cancelAnimationFrame(raf); raf = 0; }
    paint();
  }

  stage.addEventListener('pointermove', (e) => {
    if (e.pointerType !== 'mouse' || !allowed.matches) return;
    const r = svg.getBoundingClientRect();
    tx = VB.x + ((e.clientX - r.left) / r.width) * VB.width;
    ty = VB.y + ((e.clientY - r.top) / r.height) * VB.height;
    kick();
  });

  stage.addEventListener('pointerleave', () => {
    tx = REST_X;
    ty = REST_Y;
    if (allowed.matches) kick();
  });

  allowed.addEventListener('change', (e) => {
    if (!e.matches) reset();
  });
})();
