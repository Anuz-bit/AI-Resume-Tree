document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const evalId = urlParams.get('id');
    if(evalId) {
        try {
            // Mock API or actual
            // const data = await apiCall(`/results/${evalId}`);
            const mockData = {
                overall_score: 78,
                dimension_scores: { "Skill Match": 80, "Experience Quality": 65, "Career Progression": 85, "Context Fit": 82 },
                matched_requirements: [
                    {text: "3+ years Python", type: "full", node: "exp_1", reasoning: "Found 4 years of Python at Infosys."},
                    {text: "AWS Cloud", type: "partial", node: "proj_0", reasoning: "Used GCP, concepts transferrable."}
                ]
            };
            
            document.getElementById('results-skeleton').style.display = 'none';
            document.getElementById('results-content').classList.remove('hidden');
            
            animateGauge(mockData.overall_score);
            renderTree({});
            
            // Dimensions
            const dimCont = document.getElementById('dimensions-container');
            let delay = 0;
            for(let [k,v] of Object.entries(mockData.dimension_scores)) {
                let col = v>=80 ? 'bg-mint-500' : (v>=60 ? 'bg-amber-500' : 'bg-red-500');
                dimCont.innerHTML += `<div class="col gap-2">
                    <div class="row space-between text-xs"><span class="text-secondary">${k}</span><span class="font-mono font-600">${v}</span></div>
                    <div class="dim-bar-track"><div class="dim-bar-fill ${col}" style="width: 0%; transition-delay: ${delay}ms"></div></div>
                </div>`;
                delay+=100;
            }
            setTimeout(() => {
                document.querySelectorAll('.dim-bar-fill').forEach((el, i) => {
                    el.style.width = Object.values(mockData.dimension_scores)[i] + "%";
                });
            }, 100);
            
            // Reqs
            const reqCont = document.getElementById('reqs-container');
            mockData.matched_requirements.forEach(r => {
                const bType = r.type==="full" ? "badge-full" : "badge-partial";
                const bText = r.type==="full" ? "✓ Full Match" : "◐ Partial";
                reqCont.innerHTML += `<div class="card req-card ${r.type} hover:bg-elevated cursor-pointer" onclick="this.classList.toggle('open')">
                    <div class="row space-between items-center">
                        <span class="text-sm font-500">${r.text}</span>
                        <div class="row gap-2 items-center">
                            <span class="badge ${bType}">${bText}</span>
                            <span class="chip chip-${r.node.split('_')[0]}">${r.node}</span>
                            <svg class="chevron transition-transform text-tertiary" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
                        </div>
                    </div>
                    <div class="req-expand mt-4 pt-4 border-t border-border">
                        <p class="text-sm text-secondary leading-relaxed">${r.reasoning}</p>
                    </div>
                </div>`;
            });
            
        } catch(e) {}
    }
});
