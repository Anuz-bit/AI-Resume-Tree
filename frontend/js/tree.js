function renderTree(resume_tree) {
    const cont = document.getElementById('tree-container');
    cont.innerHTML = '';
    // Mock simple render
    const nodes = [
        {id: "cand", label: "Candidate", color: "green", ml: 0},
        {id: "exp_base", label: "Experience", color: "gray", ml: 16},
        {id: "exp_1", label: "Backend Engineer", color: "green", ml: 32},
        {id: "proj_base", label: "Projects", color: "gray", ml: 16},
        {id: "proj_0", label: "Accident Pred", color: "amber", ml: 32}
    ];
    nodes.forEach(n => {
        let dot = 'bg-border';
        if(n.color==='green') dot='bg-mint-500';
        if(n.color==='amber') dot='bg-amber-500';
        if(n.color==='red') dot='bg-red-500';
        
        cont.innerHTML += `<div class="tree-node" style="margin-left: ${n.ml}px">
            <div class="tree-indicator ${dot}"></div>
            <span class="chip chip-${n.id.split('_')[0]}">${n.id}</span>
            <span class="ml-2">${n.label}</span>
        </div>`;
    });
}
