/* Minimal progressive enhancement: scrolling chapters, a project filter,
   and a mobile menu. No analytics, framework, or third-party dependencies. */
(() => {
  document.documentElement.classList.add('js');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const reveal = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reducedMotion) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    }, { rootMargin: '0px 0px -36px 0px', threshold: .06 });
    reveal.forEach(el => observer.observe(el));
  } else {
    reveal.forEach(el => el.classList.add('in-view'));
  }

  const progress = document.getElementById('reading-progress');
  const navLinks = [...document.querySelectorAll('.primary-nav a')];
  const sections = navLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
  let scheduled = false;
  const updateScrollState = () => {
    const total = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    const percent = Math.min(100, Math.max(0, window.scrollY / total * 100));
    progress.style.width = `${percent}%`;
    const marker = window.scrollY + window.innerHeight * .30;
    let current = sections[0]?.id;
    sections.forEach(section => { if (section.offsetTop <= marker) current = section.id; });
    navLinks.forEach(link => {
      const active = link.getAttribute('href') === '#' + current;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current','location');
      else link.removeAttribute('aria-current');
    });
    scheduled = false;
  };
  window.addEventListener('scroll', () => {
    if (!scheduled) { requestAnimationFrame(updateScrollState); scheduled = true; }
  }, { passive: true });
  window.addEventListener('resize', updateScrollState);
  updateScrollState();

  const menuButton = document.getElementById('menu-toggle');
  const nav = document.getElementById('primary-nav');
  const closeMenu = () => {
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label','Open menu');
    nav.classList.remove('open');
  };
  menuButton.addEventListener('click', () => {
    const opening = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(opening));
    menuButton.setAttribute('aria-label', opening ? 'Close menu' : 'Open menu');
    nav.classList.toggle('open', opening);
  });
  navLinks.forEach(link => link.addEventListener('click',closeMenu));
  document.addEventListener('keydown', ev => { if (ev.key === 'Escape') closeMenu(); });
  document.addEventListener('click', ev => {
    if (!nav.contains(ev.target) && !menuButton.contains(ev.target)) closeMenu();
  });

  const filterButtons = [...document.querySelectorAll('.filter[data-filter]')];
  const projectCards = [...document.querySelectorAll('.project-card[data-kind]')];
  filterButtons.forEach(button => button.addEventListener('click', () => {
    const type = button.dataset.filter;
    filterButtons.forEach(b => {
      const selected = b === button;
      b.classList.toggle('active', selected);
      b.setAttribute('aria-pressed', String(selected));
    });
    projectCards.forEach(card => {
      card.hidden = type !== 'all' && card.dataset.kind !== type;
      if (!card.hidden) card.classList.add('in-view');
    });
  }));
})();