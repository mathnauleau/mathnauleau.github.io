// Renders "Previous Project" / "Up next" on case study pages.
// Order comes from projects.json (array order = display order, loops at both ends).
// A page only needs: <section class="project-nav container-xl col-lg-9" data-project-nav></section>
(async function () {
  const nav = document.querySelector('[data-project-nav]');
  if (!nav) return;

  const escape = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  try {
    const res = await fetch('projects.json', { cache: 'no-cache' });
    const projects = await res.json();

    // Works with /designsystem.html and GitHub Pages' /designsystem
    const current = location.pathname.split('/').pop().replace(/\.html$/, '');
    const i = projects.findIndex((p) => p.id === current);
    if (i === -1 || projects.length < 2) return;

    const prev = projects[(i - 1 + projects.length) % projects.length];
    const next = projects[(i + 1) % projects.length];

    nav.innerHTML = `
      <div class="row">
        <div class="col-6">
          <a href="${escape(prev.id)}.html" class="portfolio-link">
            <div class="prev-next left">
              <div class="col-12">
                <p class="direction"><i class="bi bi-arrow-left"></i><span data-i18n="nav.prev">Previous Project</span></p>
                <br>
                <span class="title">${escape(prev.title)}</span>
              </div>
            </div>
          </a>
        </div>
        <div class="col-6">
          <a href="${escape(next.id)}.html" class="portfolio-link">
            <div class="prev-next right">
              <div class="col-12 gx-2">
                <p class="direction"><span data-i18n="nav.next">Up next</span><i class="bi bi-arrow-right"></i></p>
                <br>
                <span class="title">${escape(next.title)}</span>
              </div>
            </div>
          </a>
        </div>
      </div>`;

    // localization.js ran before this nav existed: translate the new labels too
    if (typeof fetchLanguageData === 'function' && typeof updateContent === 'function') {
      fetchLanguageData(localStorage.getItem('language') || 'en').then(updateContent);
    }
  } catch (err) {
    console.warn('project-nav: could not load projects.json', err);
  }
})();
