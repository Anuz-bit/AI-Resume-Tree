// core.js
// Inline check to prevent flash of theme (should ideally be in HTML head, but placed here to sync everything on load)
(function() {
  const saved = localStorage.getItem('resumetree-theme');
  const system = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  const theme = saved || system;
  if (theme === 'dark') {
    document.documentElement.classList.add('dark');
  }
})();

document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Logic
  const themeToggles = document.querySelectorAll('.theme-toggle-btn');
  
  if (themeToggles.length) {
    themeToggles.forEach(btn => {
      btn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark');
        localStorage.setItem('resumetree-theme', isDark ? 'dark' : 'light');
        updateToggleIcons(isDark);
      });
    });
  }

  function updateToggleIcons(isDark) {
    document.querySelectorAll('.icon-moon').forEach(i => i.style.display = isDark ? 'none' : 'block');
    document.querySelectorAll('.icon-sun').forEach(i => i.style.display = isDark ? 'block' : 'none');
  }

  // Set initial icon state
  const isDark = document.documentElement.classList.contains('dark');
  updateToggleIcons(isDark);

  // Card Mouse Glow Effect
  const cards = document.querySelectorAll('.card.spotlight');
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });

  initReveals();
});

function initReveals() {
  try {
    const reveals = document.querySelectorAll('.animate-on-scroll');
    if (!reveals.length) return;

    const observer = new IntersectionObserver((entries, observerObj) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observerObj.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0,
      rootMargin: "0px 0px -40px 0px"
    });

    reveals.forEach(el => observer.observe(el));
  } catch(e) {
    document.querySelectorAll('.animate-on-scroll').forEach(el => el.classList.add('visible'));
    console.warn('Animation failed, showing all:', e);
  }
}
