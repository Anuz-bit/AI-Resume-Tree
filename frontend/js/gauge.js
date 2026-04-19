function animateGauge(score) {
    const arc = document.getElementById('score-arc');
    const text = document.getElementById('score-text');
    const status = document.getElementById('score-status');
    const duration = 1500;
    const start = performance.now();
    const circumference = 2 * Math.PI * 40;
    
    let colorClass = 'text-mint';
    let statusText = 'Strong Match';
    if(score < 80) { colorClass = 'text-amber'; statusText = 'Partial Match'; }
    if(score < 60) { colorClass = 'text-red'; statusText = 'Weak Match'; }
    
    arc.classList.add(colorClass); text.classList.add(colorClass); status.classList.add(colorClass);
    status.textContent = statusText;

    function update(time) {
        const elapsed = time - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const currentVal = Math.round(score * ease);
        
        text.textContent = currentVal;
        const offset = circumference - (currentVal / 100 * circumference);
        arc.style.strokeDashoffset = offset;
        
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}
