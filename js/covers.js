/* Animated project covers: only animate what can be seen.
   - A cover that leaves the viewport gets .is-paused (CSS animations freeze, see
     assets/css/covers/base.css) and its SMIL animations are paused; both resume
     where they stopped when it scrolls back in.
   - With prefers-reduced-motion, SMIL stays paused everywhere (CSS animations are
     already switched off by each cover's own reduced-motion rule).
   See assets/covers/SPEC.md. */
(function () {
  var covers = Array.prototype.slice.call(document.querySelectorAll('.portfolio-wrap > svg'));
  if (!covers.length) return;

  var reduce = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var visible = new Map();

  function apply(svg) {
    var onScreen = visible.get(svg) !== false;
    var still = reduce && reduce.matches;
    svg.classList.toggle('is-paused', !onScreen);
    if (typeof svg.pauseAnimations !== 'function') return;
    if (!onScreen || still) {
      svg.pauseAnimations();
    } else {
      svg.unpauseAnimations();
    }
  }

  function applyAll() {
    covers.forEach(apply);
  }

  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        visible.set(entry.target, entry.isIntersecting);
        apply(entry.target);
      });
    }, { rootMargin: '100px 0px' });
    covers.forEach(function (svg) {
      visible.set(svg, false);
      apply(svg);
      io.observe(svg);
    });
  } else {
    applyAll();
  }

  if (reduce) {
    if (reduce.addEventListener) reduce.addEventListener('change', applyAll);
    else if (reduce.addListener) reduce.addListener(applyAll);
  }
})();
