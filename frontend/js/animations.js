// animations.js
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('heroCanvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  let isVisible = true;

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }

  window.addEventListener('resize', resize);
  resize();

  document.addEventListener('visibilitychange', () => {
    isVisible = document.visibilityState === 'visible';
    if(isVisible) requestAnimationFrame(draw);
  });

  class Particle {
    constructor(isHub = false) {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.5; // Max 0.25px per frame roughly
      this.vy = (Math.random() - 0.5) * 0.5;
      this.isHub = isHub;
      this.radius = isHub ? 6 : Math.random() * 1 + 2; // 2-3px radius
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;
    }

    draw() {
      const isDark = document.documentElement.classList.contains('dark');
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
      ctx.fillStyle = isDark ? 'rgba(27,110,243,0.5)' : 'rgba(27,110,243,0.25)';
      ctx.fill();
    }
  }

  // 40 particles + 2 hubs
  for (let i = 0; i < 40; i++) particles.push(new Particle());
  particles.push(new Particle(true), new Particle(true));

  function draw() {
    if (!isVisible) return;
    
    ctx.clearRect(0, 0, width, height);
    
    const isDark = document.documentElement.classList.contains('dark');
    const lineStroke = isDark ? 'rgba(27,110,243,0.12)' : 'rgba(27,110,243,0.08)';

    // Update
    particles.forEach(p => p.update());

    // Draw lines
    ctx.lineWidth = 1;
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 120) {
          ctx.beginPath();
          ctx.strokeStyle = lineStroke;
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }

    // Draw points
    particles.forEach(p => p.draw());

    requestAnimationFrame(draw);
  }

  draw();
  
  // Custom Number Animate Value utility for Results Dashboard
  window.animateValue = function(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3); // cubic ease out
      obj.innerHTML = Math.floor(easeProgress * (end - start) + start);
      if (progress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    window.requestAnimationFrame(step);
  };
});
