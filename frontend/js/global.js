document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle
    const toggleBtn = document.getElementById('theme-toggle');
    const sun = document.getElementById('sun-icon');
    const moon = document.getElementById('moon-icon');
    const html = document.documentElement;
    
    // Check local storage or pref
    const isLight = localStorage.getItem('theme') === 'light';
    if(isLight) { html.classList.remove('dark'); html.classList.add('light'); sun.style.display='none'; moon.style.display='block'; }
    
    toggleBtn?.addEventListener('click', () => {
        html.classList.toggle('dark');
        html.classList.toggle('light');
        const isDark = html.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        sun.style.display = isDark ? 'block' : 'none';
        moon.style.display = isDark ? 'none' : 'block';
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const nav = document.getElementById('navbar');
        if (window.scrollY > 20) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    });

    // Observe anims
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animationPlayState = 'running';
                entry.target.classList.add('animate-in');
                if (entry.target.dataset.counter) triggerCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.2 });

    document.querySelectorAll('.scroll-fade').forEach((el, i) => {
        el.style.opacity = '0'; // hide initially
        el.style.animationDelay = `${(i%5)*80}ms`;
        observer.observe(el);
    });
});

function triggerCounter(el) {
    const target = parseInt(el.dataset.counter, 10);
    const duration = 1200;
    const start = performance.now();
    const isDecimal = el.dataset.counter.includes('.');
    
    function update(time) {
        const elapsed = time - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3); // ease out cubic
        const current = target * ease;
        el.textContent = isDecimal ? current.toFixed(2) : Math.floor(current);
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target;
    }
    requestAnimationFrame(update);
}

function showToast(message, type='info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<div class="row items-center gap-2"><div class="text-sm font-500">${message}</div></div><div class="toast-progress"></div>`;
    container.appendChild(toast);
    
    const progress = toast.querySelector('.toast-progress');
    // Animate progress shrink 4s
    progress.style.transitionDuration = '4s';
    requestAnimationFrame(() => { progress.style.width = '0%'; });
    
    setTimeout(() => {
        toast.classList.add('out');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
