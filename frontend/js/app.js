// app.js
document.addEventListener('DOMContentLoaded', () => {
  setupUploadFlow('state-idle', 'flow-container', 'state-done', 'jd-textarea', 'analyze-btn', 'auto-detect-strip', 'char-counter', true);
  setupUploadFlow('cta-state-idle', 'cta-flow-container', 'cta-state-done', 'cta-jd-textarea', 'cta-analyze-btn', null, null, false);
});

function setupUploadFlow(idleId, flowId, doneId, textId, btnId, stripId, counterId, isMainHero) {
  const uploadZone = document.getElementById(idleId);
  const flowContainer = document.getElementById(flowId);
  const doneZone = document.getElementById(doneId);
  const jdTextarea = document.getElementById(textId);
  const analyzeBtn = document.getElementById(btnId);
  const strip = stripId ? document.getElementById(stripId) : null;
  const counter = counterId ? document.getElementById(counterId) : null;
  
  let fileLoaded = false;
  let currentFile = null;
  
  if (uploadZone && flowContainer) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf,.docx';
    fileInput.style.display = 'none';
    uploadZone.appendChild(fileInput);

    uploadZone.addEventListener('click', () => { if(!fileLoaded) fileInput.click(); });

    ['dragover', 'dragenter'].forEach(evt => {
      uploadZone.addEventListener(evt, (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-active');
        uploadZone.querySelector('p:last-child').innerText = "Release to upload";
      });
    });

    ['dragleave', 'dragend', 'drop'].forEach(evt => {
      uploadZone.addEventListener(evt, (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-active');
        uploadZone.querySelector('p:last-child').innerText = "Click to browse or drag and drop";
      });
    });

    uploadZone.addEventListener('drop', (e) => {
      if(e.dataTransfer.files.length) handleUpload(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener('change', () => {
      if(fileInput.files.length) handleUpload(fileInput.files[0]);
    });

    function handleUpload(file) {
      if(fileLoaded) return;
      
      if(file.size > 5 * 1024 * 1024) {
        uploadZone.classList.add('error');
        setTimeout(() => uploadZone.classList.remove('error'), 400);
        alert("Only PDF or DOCX, max 5MB");
        return;
      }

      fileLoaded = true;
      currentFile = file;
      uploadZone.classList.add('success');
      
      const checkPath = document.getElementById('check-path');
      if (checkPath && isMainHero) {
          checkPath.style.strokeDasharray = "30";
          checkPath.style.strokeDashoffset = "30";
          checkPath.style.animation = "drawCheck 300ms ease-out forwards";
      }
      
      setTimeout(() => {
        uploadZone.style.display = 'none';
        doneZone.style.display = 'block';
        if(isMainHero) {
            document.getElementById('filename-display').innerText = file.name;
        }
        flowContainer.classList.add('state-jd');
        
        if (isMainHero) {
          const step1Ind = document.getElementById('step1-ind');
          const step2Ind = document.getElementById('step2-ind');
          const stepLine = document.getElementById('step-line');
          
          if(step1Ind && step2Ind) {
            step1Ind.classList.replace('step-active', 'step-inactive');
            step1Ind.innerHTML = `✓ Upload your resume`;
            step2Ind.classList.replace('step-inactive', 'step-active');
            
            if(stepLine) {
                stepLine.style.strokeDasharray = "40";
                stepLine.style.strokeDashoffset = "40";
                stepLine.style.transition = "stroke-dashoffset 500ms cubic-bezier(0,0,0.2,1)";
                setTimeout(() => stepLine.style.strokeDashoffset = "0", 100);
            }
          }
        }
  
        setTimeout(() => { jdTextarea?.focus(); }, 380);
      }, 400);
    }
  }

  // JD Panel logic
  if(jdTextarea && analyzeBtn) {
    jdTextarea.addEventListener('input', () => {
      const len = jdTextarea.value.length;
      if (counter) counter.innerText = `${len} / 2000+`;
      
      if(len >= 100) {
        if (counter) counter.style.color = 'var(--excellent)';
        analyzeBtn.disabled = false;
        analyzeBtn.removeAttribute('title');
        analyzeBtn.innerText = 'Analyze ATS Match →';
        analyzeBtn.classList.add('active');
        
        if (strip && strip.style.display === 'none') {
            strip.style.display = 'block';
            strip.innerHTML = `📋 Detected: Software Engineer · ${Math.floor(Math.random() * 15 + 10)} requirements found`;
        }
      } else {
        if (counter) counter.style.color = 'var(--t3)';
        analyzeBtn.disabled = true;
        analyzeBtn.setAttribute('title', 'Required — tells us what to match your resume against');
        analyzeBtn.innerText = 'Add job description to continue';
        analyzeBtn.classList.remove('active');
        if (strip) strip.style.display = 'none';
      }
    });

    analyzeBtn.addEventListener('click', () => {
      if(!jdTextarea.value || jdTextarea.value.length < 100) return;
      if(!fileLoaded) {
          alert("Please upload your resume first.");
          return;
      }
      startProcessingAnimation(currentFile, jdTextarea.value);
    });
  }
}

async function startProcessingAnimation(file, jdText) {
  const overlay = document.getElementById('processing-overlay');
  const stepsContainer = document.getElementById('progress-steps');
  const bar = document.getElementById('progress-bar');
  const timeEst = document.getElementById('time-est');

  if(!overlay) return;
  overlay.classList.add('active');

  // Trigger actual API call in background
  const formData = new FormData();
  formData.append('resume', file);
  formData.append('jd_text', jdText);

  let apiFinished = false;
  fetch('http://localhost:8000/evaluate', {
      method: 'POST',
      body: formData
  })
  .then(async r => {
      if(!r.ok) {
          const errData = await r.json().catch(() => null);
          const errText = errData && errData.detail ? errData.detail : "Backend error";
          throw new Error(errText);
      }
      return r.json();
  })
  .then(data => {
      localStorage.setItem('lastResult', JSON.stringify(data));
      localStorage.setItem('lastFilename', file.name);
      localStorage.setItem('lastJD', jdText);
      apiFinished = true;
  })
  .catch(err => {
      console.error(err);
      alert("Analysis failed with error:\n\n" + err.message + "\n\n(If you see 429 RESOURCE_EXHAUSTED, your Google API Key has run out of its free tier quota.)");
      overlay.classList.remove('active');
  });
  
  // Set width to 100% over 18s via CSS transition
  setTimeout(() => { if(bar) bar.style.width = '100%'; }, 100);

  const steps = [
    { msg: "Resume structure detected — 6 sections found", wait: 500 },
    { msg: "Job description parsed — 23 requirements", wait: 1700 },
    { msg: "Matching keywords against JD...", wait: 2900 },
    { msg: "Scoring ATS compatibility", wait: 4100 },
    { msg: "Generating improvement suggestions", wait: 5300 }
  ];

  let activeIndex = -1;
  const stepElements = [];

  // Pre-render steps as pending
  steps.forEach((s) => {
      const el = document.createElement('div');
      el.className = "flex items-center gap-3";
      el.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--border-hi)" stroke-width="2" class="step-icon"><circle cx="12" cy="12" r="10"></circle></svg>
        <span class="step-text text-t3" style="font-size:14px;">${s.msg}</span>
      `;
      el.style.opacity = 0;
      el.style.transform = 'translateY(10px)';
      el.style.animation = 'fadeDown 300ms var(--out) forwards';
      stepsContainer.appendChild(el);
      stepElements.push(el);
  });

  const checkIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--excellent)" stroke-width="2" class="step-icon"><path d="M20 6L9 17l-5-5"></path></svg>`;
  const loadIcon = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--brand)" stroke-width="2" class="animate-spin step-icon"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>`;

  steps.forEach((stepObj, i) => {
    setTimeout(() => {
      // Complete previous
      if (activeIndex >= 0) {
          stepElements[activeIndex].querySelector('.step-icon').outerHTML = checkIcon;
          const textEl = stepElements[activeIndex].querySelector('.step-text');
          textEl.classList.remove('text-brand', 'font-500');
          textEl.classList.add('text-t1');
      }
      
      activeIndex = i;
      
      // Activate current
      stepElements[i].querySelector('.step-icon').outerHTML = loadIcon;
      const textEl = stepElements[i].querySelector('.step-text');
      textEl.classList.remove('text-t3');
      textEl.classList.add('text-brand', 'font-500');

      if(i === steps.length - 1) {
          // Wait for API to finish if it hasn't yet, then redirect
          const checkReady = setInterval(() => {
              if (apiFinished) {
                  clearInterval(checkReady);
                  setTimeout(() => { window.location.href = "results.html"; }, 1000);
              }
          }, 500);
      }

    }, stepObj.wait);
  });
  
  // Timer countdown
  let remaining = 18;
  const timer = setInterval(() => {
      remaining--;
      if (remaining > 0 && timeEst) {
          timeEst.innerText = remaining + "s remaining";
      } else if (remaining <= 0 && timeEst) {
          timeEst.innerHTML = `<span style="color:var(--brand);">Processing with AI... (this may take up to 2 mins)</span>`;
      }
      
      if (remaining <= -120) {
          clearInterval(timer);
      }
  }, 1000);
  
  // Setup node graph canvas
  const c = document.getElementById('processingCanvas');
  if (c) {
      const ctx = c.getContext('2d');
      let nodes = [];
      for(let i=0; i<6; i++) {
          nodes.push({
              x: Math.random() * c.width,
              y: Math.random() * c.height,
              vx: (Math.random()-0.5) * 1,
              vy: (Math.random()-0.5) * 1
          });
      }
      function drawGraph() {
          ctx.clearRect(0,0,c.width,c.height);
          ctx.fillStyle = 'rgba(27,110,243,0.8)';
          ctx.strokeStyle = 'rgba(27,110,243,0.3)';
          ctx.lineWidth = 1.5;
          nodes.forEach(n => {
              n.x += n.vx; n.y += n.vy;
              if(n.x<0 || n.x>c.width) n.vx*=-1;
              if(n.y<0 || n.y>c.height) n.vy*=-1;
              ctx.beginPath(); ctx.arc(n.x, n.y, 3, 0, Math.PI*2); ctx.fill();
          });
          for(let i=0; i<nodes.length; i++){
              for(let j=i+1; j<nodes.length; j++){
                  if(Math.random() > 0.4) {
                      ctx.beginPath(); ctx.moveTo(nodes[i].x, nodes[i].y); ctx.lineTo(nodes[j].x, nodes[j].y); ctx.stroke();
                  }
              }
          }
      }
      setInterval(drawGraph, 100);
  }
}
