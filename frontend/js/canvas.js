const canvasContainer = document.getElementById('hero-canvas');
if (canvasContainer) {
    const cvs = document.createElement('canvas');
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    canvasContainer.appendChild(cvs);
    const ctx = cvs.getContext('2d');
    
    let animId;
    let nodes = [];
    
    // Create regular nodes
    for (let i = 0; i < 40; i++) {
        nodes.push({
            x: Math.random() * cvs.width,
            y: Math.random() * cvs.height,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            r: Math.random() + 2, // 2-3px
            hub: false
        });
    }
    // Create 2 hub nodes
    for (let i = 0; i < 2; i++) {
        nodes.push({
            x: Math.random() * cvs.width,
            y: Math.random() * cvs.height,
            vx: (Math.random() - 0.5) * 0.2, // 0.1px speed
            vy: (Math.random() - 0.5) * 0.2,
            r: 5,
            hub: true
        });
    }
    
    function draw() {
        const isDark = document.documentElement.classList.contains('dark');
        const particleColor = isDark ? 'rgba(27,110,243,0.55)' : 'rgba(27,110,243,0.45)';
        const lineColor = isDark ? 'rgba(27,110,243,0.15)' : 'rgba(27,110,243,0.10)';

        ctx.clearRect(0, 0, cvs.width, cvs.height);
        ctx.lineWidth = 0.8;
        
        nodes.forEach(n => {
            n.x += n.vx;
            n.y += n.vy;
            if (n.x < 0 || n.x > cvs.width) n.vx *= -1;
            if (n.y < 0 || n.y > cvs.height) n.vy *= -1;
            
            ctx.fillStyle = particleColor;
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
            ctx.fill();
        });
        
        ctx.strokeStyle = lineColor;
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 130) {
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.stroke();
                }
            }
        }
        
        animId = requestAnimationFrame(draw);
    }
    
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            cancelAnimationFrame(animId);
        } else {
            draw();
        }
    });
    
    draw();
    
    window.addEventListener('resize', () => {
        cvs.width = window.innerWidth;
        cvs.height = window.innerHeight;
    });
}
