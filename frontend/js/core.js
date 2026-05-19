// core.js
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

  // Navbar Scroll
  window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if(navbar) navbar.classList.toggle('scrolled', window.scrollY > 20);
  });

  initReveals();
});

function initReveals() {
  const reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;

  const observer = new IntersectionObserver((entries, observerObj) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        
        // Trigger counters if they exist in this section
        const counters = entry.target.querySelectorAll('.stat-num');
        counters.forEach(triggerCounter);

        observerObj.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0,
    rootMargin: "0px 0px -40px 0px"
  });

  reveals.forEach(el => observer.observe(el));
}

function triggerCounter(el) {
  if (el.dataset.animated) return;
  el.dataset.animated = "true";
  
  const target = parseInt(el.getAttribute('data-target'), 10);
  if (isNaN(target)) return;

  const duration = 1200; // 1200ms
  const start = performance.now();
  
  function update(time) {
      const elapsed = time - start;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const current = target * ease;
      
      // format logic (add commas for big numbers)
      el.textContent = Math.floor(current).toLocaleString();
      
      if (progress < 1) requestAnimationFrame(update);
      else el.textContent = target.toLocaleString();
  }
  requestAnimationFrame(update);
}
