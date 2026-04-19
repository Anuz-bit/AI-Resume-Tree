const canvasContainer = document.getElementById('hero-canvas');
if(canvasContainer) {
    const cvs = document.createElement('canvas');
    cvs.width = window.innerWidth; cvs.height = window.innerHeight;
    canvasContainer.appendChild(cvs);
    const ctx = cvs.getContext('2d');
    
    let nodes = [];
    for(let i=0; i<35; i++) {
        nodes.push({
            x: Math.random() * cvs.width,
            y: Math.random() * cvs.height,
            vx: (Math.random()-0.5) * 0.3,
            vy: (Math.random()-0.5) * 0.3
        });
    }
    
    function draw() {
        ctx.clearRect(0,0,cvs.width,cvs.height);
        ctx.fillStyle = 'rgba(37,99,235,0.4)';
        ctx.strokeStyle = 'rgba(37,99,235,0.12)';
        ctx.lineWidth = 1;
        
        nodes.forEach(n => {
            n.x += n.vx; n.y += n.vy;
            if(n.x<0 || n.x>cvs.width) n.vx*=-1;
            if(n.y<0 || n.y>cvs.height) n.vy*=-1;
            ctx.beginPath(); ctx.arc(n.x, n.y, 2, 0, Math.PI*2); ctx.fill();
        });
        
        for(let i=0; i<nodes.length; i++){
            for(let j=i+1; j<nodes.length; j++){
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if(dist < 120) {
                    ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(nodes[j].x, nodes[j].y); ctx.stroke();
                }
            }
        }
        if(!document.hidden) requestAnimationFrame(draw);
    }
    document.addEventListener('visibilitychange', () => { if(!document.hidden) requestAnimationFrame(draw); });
    draw();
    window.addEventListener('resize', () => { cvs.width = window.innerWidth; cvs.height = window.innerHeight; });
}
