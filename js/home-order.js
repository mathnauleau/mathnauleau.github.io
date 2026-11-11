// Re-sorts the homepage cards to match projects.json (array order = display order).
// The cards stay real HTML in index.html: this only moves them, cards not in projects.json go last.
// index.html has two .portfolio-container grids (work, side projects): each one is sorted on its own.
(async function () {
  const containers = document.querySelectorAll('.portfolio-container');

  containers.forEach((container) => {
    container.style.visibility = 'hidden';
  });

  const cardId = (card) => {
    const link = card.querySelector('a.portfolio-link');
    return link ? link.getAttribute('href').replace(/\.html$/, '') : null;
  };

  try {
    const res = await fetch('projects.json', { cache: 'no-cache' });
    const projects = await res.json();
    const ids = projects.map((p) => p.id);
    const rank = (card) => {
      const i = ids.indexOf(cardId(card));
      return i === -1 ? ids.length : i;
    };

    containers.forEach((container) => {
      const cards = Array.from(container.querySelectorAll(':scope > .portfolio-item'));
      cards.sort((a, b) => rank(a) - rank(b)).forEach((card) => container.appendChild(card));

      // main.js creates Isotope on window load, which can land before or after this fetch.
      // Not created yet: Isotope will read the new order itself.
      const iso = window.Isotope && Isotope.data(container);
      if (iso) {
        iso.reloadItems();
        iso.arrange();
      }
    });
  } catch (err) {
    console.warn('home-order: could not load projects.json', err);
  } finally {
    containers.forEach((container) => {
      container.style.visibility = '';
    });
  }
})();
