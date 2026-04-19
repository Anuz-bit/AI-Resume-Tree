const zone = document.getElementById('upload-zone');
const input = document.getElementById('resume-input');
const title = document.getElementById('upload-title');
const desc = document.getElementById('upload-desc');
const evaluateBtn = document.getElementById('evaluate-btn');
const jdInput = document.getElementById('jd-input');
let file = null;

function updateState() { if(file && jdInput.value.length > 20) evaluateBtn.disabled = false; else evaluateBtn.disabled = true; }

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(ev => zone.addEventListener(ev, e => { e.preventDefault(); e.stopPropagation(); }));
['dragenter', 'dragover'].forEach(ev => zone.addEventListener(ev, () => { zone.classList.add('dragover'); title.textContent = "Release to upload"; }));
['dragleave', 'drop'].forEach(ev => zone.addEventListener(ev, () => { zone.classList.remove('dragover'); }));

zone.addEventListener('drop', e => {
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
});
input.addEventListener('change', e => { handleFile(e.target.files[0]); });
jdInput.addEventListener('input', updateState);

function handleFile(f) {
    if(!f) return;
    if(!f.name.endsWith('.pdf') && !f.name.endsWith('.docx')) {
        zone.classList.add('error'); setTimeout(()=>zone.classList.remove('error'), 500);
        showToast("Invalid file type. Please use PDF or DOCX.", "error"); return;
    }
    file = f;
    zone.classList.add('loaded');
    title.textContent = f.name;
    desc.textContent = (f.size / 1024 / 1024).toFixed(2) + " MB";
    title.classList.add('text-mint');
    updateState();
}

evaluateBtn.addEventListener('click', async () => {
    if(!file || !jdInput.value) return;
    const overlay = document.getElementById('progress-overlay');
    overlay.classList.add('show');
    const steps = document.querySelectorAll('.step');
    const fill = document.getElementById('progress-fill');
    
    // Simulate steps graphically
    let currentStep = 0;
    const stepInterval = setInterval(() => {
        if(currentStep < steps.length) {
            steps.forEach((s, i) => {
                if(i < currentStep) s.textContent = s.textContent.replace('○', '✓');
                if(i === currentStep) { s.classList.remove('opacity-50'); fill.style.width = s.dataset.pct + "%"; }
            });
            currentStep++;
        }
    }, 1500);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('jd_text', jdInput.value);

    try {
        const res = await apiCall('/evaluate', 'POST', formData);
        clearInterval(stepInterval);
        fill.style.width = "100%";
        steps.forEach(s => s.textContent = s.textContent.replace('○', '✓'));
        setTimeout(() => { window.location.href = `results.html?id=${res.eval_id || 'test_id'}`; }, 800);
    } catch(err) {
        clearInterval(stepInterval);
        overlay.classList.remove('show');
    }
});
