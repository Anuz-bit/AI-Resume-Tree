// app.js
document.addEventListener('DOMContentLoaded', () => {
  const uploadZone = document.getElementById('state-idle');
  const flowContainer = document.getElementById('flow-container');
  const step1Ind = document.getElementById('step1-ind');
  const step2Ind = document.getElementById('step2-ind');
  
  let fileLoaded = false;
  
  if (uploadZone && flowContainer) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf,.docx';
    fileInput.style.display = 'none';
    uploadZone.appendChild(fileInput);

    uploadZone.addEventListener('click', () => {
      if(!fileLoaded) fileInput.click();
    });

    ['dragover', 'dragenter'].forEach(evt => {
      uploadZone.addEventListener(evt, (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-active');
      });
    });

    ['dragleave', 'dragend', 'drop'].forEach(evt => {
      uploadZone.addEventListener(evt, (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-active');
      });
    });

    uploadZone.addEventListener('drop', (e) => {
      if(e.dataTransfer.files.length) {
        handleUpload(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', () => {
      if(fileInput.files.length) {
        handleUpload(fileInput.files[0]);
      }
    });

    function handleUpload(file) {
      if(fileLoaded) return;
      
      if(file.size > 5 * 1024 * 1024) {
        alert("File too large. Max 5MB.");
        return;
      }

      fileLoaded = true;
      
      document.getElementById('state-idle').style.display = 'none';
      document.getElementById('state-done').style.display = 'block';
      flowContainer.classList.add('state-jd');
      
      if(step1Ind && step2Ind) {
        step1Ind.classList.replace('step-active', 'step-inactive');
        step2Ind.classList.replace('step-inactive', 'step-active');
      }

      setTimeout(() => {
        document.getElementById('jd-textarea')?.focus();
      }, 400);
    }
  }

  // JD Panel logic
  const jdTextarea = document.getElementById('jd-textarea');
  const counter = document.getElementById('char-counter');
  const analyzeBtn = document.getElementById('analyze-btn');

  if(jdTextarea && analyzeBtn) {
    jdTextarea.addEventListener('input', () => {
      const len = jdTextarea.value.length;
      counter.innerText = `${len} / 2000+`;
      
      if(len >= 100) {
        counter.style.color = 'var(--excellent)';
        analyzeBtn.disabled = false;
        analyzeBtn.removeAttribute('title');
        analyzeBtn.innerText = 'Analyze ATS Match →';
        analyzeBtn.style.background = 'linear-gradient(135deg, var(--brand), var(--brand-hi))';
        analyzeBtn.style.color = '#fff';
        analyzeBtn.style.border = 'none';
        
        // Single pulse effect
        analyzeBtn.style.boxShadow = "0 0 0 4px var(--brand-glow)";
        setTimeout(() => analyzeBtn.style.boxShadow = "none", 1000);
      } else {
        counter.style.color = 'var(--t3)';
        analyzeBtn.disabled = true;
        analyzeBtn.setAttribute('title', 'Required — tells us what to match your resume against');
        analyzeBtn.innerText = 'Add job description to continue';
        analyzeBtn.style.background = 'var(--border)';
        analyzeBtn.style.color = 'var(--t3)';
      }
    });

    analyzeBtn.addEventListener('click', () => {
      if(!jdTextarea.value || jdTextarea.value.length < 100) return;
      startProcessingAnimation();
    });
  }

  function startProcessingAnimation() {
    const overlay = document.getElementById('processing-overlay');
    const stepsContainer = document.getElementById('progress-steps');
    const bar = document.getElementById('progress-bar');
    const timeEst = document.getElementById('time-est');

    if(!overlay) return;
    
    overlay.classList.add('active');
    setTimeout(() => { if(bar) bar.style.width = '100%'; }, 100);

    const checkIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--excellent)" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    const loadIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="animate-spin" style="opacity:0.5"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>`;

    const steps = [
      { msg: "Resume structure detected (6 sections)", wait: 500 },
      { msg: "Job description parsed (23 requirements)", wait: 1700 },
      { msg: "Matching keywords against JD...", wait: 2800 },
      { msg: "Scoring ATS compatibility", wait: 4000 },
      { msg: "Generating improvement suggestions", wait: 5200 },
      { msg: "Finalizing report", wait: 6000 }
    ];

    let currentStepEl = null;

    steps.forEach((stepObj, i) => {
      setTimeout(() => {
        if(currentStepEl) {
          currentStepEl.innerHTML = `<div class="flex items-center gap-2">${checkIcon} <span class="text-t2" style="font-size:14px;">${currentStepEl.getAttribute('data-msg')}</span></div>`;
        }

        currentStepEl = document.createElement('div');
        currentStepEl.setAttribute('data-msg', stepObj.msg);
        currentStepEl.innerHTML = `<div class="flex items-center gap-2">${loadIcon} <span class="text-t1 font-500" style="font-size:14px;">${stepObj.msg}</span></div>`;
        currentStepEl.style.opacity = 0;
        currentStepEl.style.transform = 'translateY(10px)';
        currentStepEl.style.transition = 'all 200ms ease';
        stepsContainer.appendChild(currentStepEl);
        
        void currentStepEl.offsetWidth;
        currentStepEl.style.opacity = 1;
        currentStepEl.style.transform = 'translateY(0)';

        timeEst.innerText = Math.max(0, 18 - Math.floor(stepObj.wait/300));

        if(i === steps.length - 1) {
          setTimeout(() => { window.location.href = "results.html"; }, 800);
        }

      }, stepObj.wait);
    });
  }

  // Dashboard logic: trigger gauge on load
  const gaugeWrapper = document.getElementById('hero-gauge');
  if(gaugeWrapper && window.animateValue) {
    const gaugeCta = document.getElementById('gauge-score');
    const target = parseInt(gaugeCta.getAttribute('data-score') || 82);
    const circle = document.getElementById('gauge-circle');
    
    setTimeout(() => {
      if(circle) {
        const circumference = 2 * Math.PI * 110;
        circle.style.strokeDasharray = `${circumference}`;
        circle.style.strokeDashoffset = `${circumference}`;
        
        let targetOffset = circumference - (target / 100) * circumference;
        circle.style.transition = `stroke-dashoffset 1400ms cubic-bezier(0,0,0.2,1)`;
        circle.style.strokeDashoffset = targetOffset;
      }
    }, 200);

    window.animateValue(gaugeCta, 0, target, 1400);

    document.querySelectorAll('.dim-bar-fill').forEach((bar, i) => {
      const w = bar.getAttribute('data-width');
      bar.style.width = '0%';
      setTimeout(() => {
        bar.style.transition = 'width 700ms cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        bar.style.width = w;
      }, 500 + (i * 120));
    });
  }
});
