const runas = {
    hmm: { 
        nome: "Heavy Magic Missile",
        mana: 70,
        imagem: "hmm.gif",
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid", "Paladin", "Royal Paladin"] 
    },
    uh: { 
        nome: "Ultimate Healing", 
        mana: 100, 
        imagem: "uh.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    sd: { 
        nome: "Sudden Death", 
        mana: 220, 
        imagem: "sd.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer"] 
    },
    gfb: { 
        nome: "Great Fireball", 
        mana: 120,
        imagem: "gfb.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    enve: { 
        nome: "Envenom",
        mana: 100, 
        imagem: "envenom.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    }, 
    explo: { 
        nome: "Explosion", 
        mana: 180, 
        imagem: "explo.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    ad: { 
        nome: "Animate Dead", 
        mana: 300, 
        imagem: "animatedead.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    at: { 
        nome: "Antidote", 
        mana: 50, 
        imagem: "antidote.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    ch: { 
        nome: "Chameleon", 
        mana: 150, 
        imagem: "chameleon.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    cc: { 
        nome: "Convince Creature", 
        mana: 100, 
        imagem: "convincecreature.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    dst: { 
        nome: "Desintegrate", 
        mana: 100,
        imagem: "desintegrate.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid", "Paladin", "Royal Paladin"] 
    },
    df: { 
        nome: "Destroy Field", 
        mana: 60,
        imagem: "destroyfield.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid", "Paladin", "Royal Paladin"] 
    },
    ef: { 
        nome: "Energy Field", 
        mana: 80,
        imagem: "energyfield.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    ew: {
        nome: "Energy Wall", 
        mana: 250,
        imagem: "energywall.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    eb: { 
        nome: "Energy Bomb", 
        mana: 220,
        imagem: "energybomb.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer"] 
    },
    ff: { 
        nome: "Fire Field", 
        mana: 60,
        imagem: "firefield.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    fw: { 
        nome: "Fire Wall", 
        mana: 200,
        imagem: "firewall.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    fireb: { 
        nome: "Fireball", 
        mana: 60,
        imagem: "fireball.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid", "Paladin", "Royal Paladin"] 
    },
    fb: { 
        nome: "Fire Bomb", 
        mana: 150,
        imagem: "firebomb.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    },
    ih: {
        nome: "Intense Healing", 
        mana: 60,
        imagem: "ih.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    lmm: { 
        nome: "Light Magic Missile", 
        mana: 40,
        imagem: "lmm.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid", "Paladin", "Royal Paladin"] 
    },
    mw: { 
        nome: "Magic Wall", 
        mana: 250,
        imagem: "magicwall.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer"] 
    },
    pr: { 
        nome: "Paralyze", 
        mana: 600,
        imagem: "paralyze.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    pf: { 
        nome: "Poison Field", 
        mana: 50,
        imagem: "poisonfield.gif", 
        vocacoes: ["Druid", "Elder Druid", "Sorcerer", "Master Sorcerer"] 
    },
    pw: { 
        nome: "Poison Wall", 
        mana: 160,
        imagem: "poisonwall.gif", 
        vocacoes: ["Druid", "Elder Druid", "Sorcerer", "Master Sorcerer"] 
    },
    pb: { 
        nome: "Poison Bomb", 
        mana: 130,
        imagem: "poisonbomb.gif", 
        vocacoes: ["Druid", "Elder Druid"] 
    },
    sf: { 
        nome: "Soulfire", 
        mana: 150,
        imagem: "soulfire.gif", 
        vocacoes: ["Sorcerer", "Master Sorcerer", "Druid", "Elder Druid"] 
    }

};

const vocacoes = {
    "Sorcerer": 1/6,
    "Master Sorcerer": 1/4,
    "Druid": 1/6,
    "Elder Druid": 1/4,
    "Paladin": 1/8,
    "Royal Paladin": 1/6
};

const foods = {
    d_ham: { nome: "Dragon Ham", duracao: 720, imagem: "d_ham.gif" },
    orange: { nome: "Orange", duracao: 156, imagem: "orange.gif" },
    fish: { nome: "Fish", duracao: 144, imagem: "fish.gif" }
};


function atualizarRuna() {
    const runaSelecionada = document.getElementById("runa").value;
    const vocacaoSelect = document.getElementById("vocacao");
    const runa = runas[runaSelecionada];

    // Atualiza imagem da runa
    document.getElementById("runaImg").src = runa.imagem;

    // Atualiza lista de vocações permitidas
    vocacaoSelect.innerHTML = "";
    runa.vocacoes.forEach(v => {
        const opt = document.createElement("option");
        opt.value = v;
        opt.textContent = v;
        vocacaoSelect.appendChild(opt);
    });

    calcularTempo();
}

function calcularTempo() {
    const runaSelecionada = document.getElementById("runa").value;
    const vocacaoSelecionada = document.getElementById("vocacao").value;
    const foodSelecionada = document.getElementById("food").value; 

    if (!runaSelecionada || !vocacaoSelecionada) return;

    const runa = runas[runaSelecionada];
    const regen = vocacoes[vocacaoSelecionada];
    
    // Calcula tempo em segundos
    const tempoRunaSeg = runa.mana / regen; 
    
    const tempoBP = tempoRunaSeg * 20;

    document.getElementById("tempoRuna").textContent = `Tempo para 1 runa: ${formatarTempo(tempoRunaSeg)}`;
    document.getElementById("tempoBP").textContent = `Tempo para 1 backpack: ${formatarTempo(tempoBP)}`;

    // --- CÁLCULO E EXIBIÇÃO DA FOOD ---
    
    // 1. As variáveis precisam ser definidas ANTES de serem usadas!
    const food = foods[foodSelecionada];
    const foodsNecessarias = Math.ceil(tempoBP / food.duracao);
    
    // 2. Atualizar a imagem da food e mostrar
    const foodImgElement = document.getElementById("foodImg");
    foodImgElement.src = food.imagem;
    foodImgElement.style.display = 'inline-block';
    
    // 3. ATUALIZA A QUANTIDADE: Usa o novo ID "foodBP_quantity" para mostrar SÓ a quantidade.
    document.getElementById("foodBP_quantity").textContent =
        `${foodsNecessarias} ${food.nome}${foodsNecessarias > 1 ? "s" : ""}`;
    
    // Nota: O título "Foods necessárias para 1 BP:" agora é um elemento estático no HTML (foodBP_title) 
    // e não precisa ser preenchido pelo JS.

}


function formatarTempo(segundos) {
    const h = Math.floor(segundos / 3600);
    const m = Math.floor((segundos % 3600) / 60);
    const s = Math.floor(segundos % 60);
    return `${h}h ${m}m ${s}s`;
}

function popularFoods() {
    const foodSelect = document.getElementById("food");
    foodSelect.innerHTML = ""; // Limpa qualquer opção existente

    // Itera sobre todas as keys (d_ham, orange, b_mush, etc) no objeto foods
    for (const key in foods) {
        const food = foods[key];
        const opt = document.createElement("option");
        opt.value = key; // O valor será 'd_ham', 'orange', etc.
        opt.textContent = food.nome; // O texto será 'Dragon Ham', 'Orange', etc.
        foodSelect.appendChild(opt);
    }
}

function popularRunas() {
    const runaSelect = document.getElementById("runa");
    runaSelect.innerHTML = ""; // Limpa qualquer opção existente

    // Itera sobre todas as keys (hmm, uh, etc) no objeto runas
    for (const key in runas) {
        const runa = runas[key];
        const opt = document.createElement("option");
        opt.value = key; // O valor será 'hmm', 'uh', etc.
        opt.textContent = runa.nome; // O texto será 'Heavy Magic Missile', etc.
        runaSelect.appendChild(opt);
    }
}

// Inicialização
document.getElementById("runa").addEventListener("change", atualizarRuna);
document.getElementById("vocacao").addEventListener("change", calcularTempo);
document.getElementById("food").addEventListener("change", calcularTempo);
popularRunas();
popularFoods();
atualizarRuna();