// =================================================================
// DADOS BASE E RUNAS
// =================================================================

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


// =================================================================
// DADOS DE REGENERAÇÃO DE MANA EXTRA (NOVOS)
// As taxas são Mana por Segundo (M/S) e Duração em Segundos (S)
// =================================================================

const REGEN_BOOSTS = {
    giantSaphire: { nome: "Giant Saphire Amulet", duracao: 5400, regen_ms: 1/3 }, // 1 mana/3s. Duração: 1h30m = 5400s
    lifeRing: { nome: "Life Ring", duracao: 1200, regen_ms: 1/3 }, // 1 mana/3s. Duração: 20m = 1200s
    ringOfHealing: { nome: "Ring of Healing", duracao: 450, regen_ms: 1/1 } // 1 mana/1s. Duração: 7m30s = 450s
};


// =================================================================
// FUNÇÕES DE CONTROLE E UI
// =================================================================

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

    popularFoods();
    calcularTempo();
}

function popularRunas() {
    const runaSelect = document.getElementById("runa");
    runaSelect.innerHTML = ""; 

    for (const key in runas) {
        const runa = runas[key];
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = runa.nome;
        runaSelect.appendChild(opt);
    }
}

function popularFoods() {
    const foodSelect = document.getElementById("food");
    foodSelect.innerHTML = ""; 

    for (const key in foods) {
        const food = foods[key];
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = food.nome;
        foodSelect.appendChild(opt);
    }
}


// NOVO: Função para garantir que apenas um ring de regen esteja selecionado
function handleRingExclusivity(changedId) {
    const lifeRing = document.getElementById('lifeRing');
    const ringOfHealing = document.getElementById('ringOfHealing');

    // Regra: Os dois rings são mutuamente exclusivos.
    
    // Se o Life Ring foi clicado e está checado, desmarca o Ring of Healing
    if (changedId === 'lifeRing' && lifeRing.checked) {
        ringOfHealing.checked = false;
    }
    
    // Se o Ring of Healing foi clicado e está checado, desmarca o Life Ring
    else if (changedId === 'ringOfHealing' && ringOfHealing.checked) {
        lifeRing.checked = false;
    }

    // Depois de garantir a exclusividade, chama a função de cálculo principal
    calcularTempo();
}


// =================================================================
// LÓGICA PRINCIPAL DE CÁLCULO (REESCRITA PARA INCLUIR BOOSTS)
// =================================================================

function calcularTempo() {
    const runaSelecionada = document.getElementById("runa").value;
    const vocacaoSelecionada = document.getElementById("vocacao").value;
    const foodSelecionada = document.getElementById("food").value; 

    // --- 1. COLETA DE ESTADO DOS BOOSTS E CONTROLES ---
    const checkSaphire = document.getElementById("giantSaphire");
    const checkLifeRing = document.getElementById("lifeRing");
    const checkRoH = document.getElementById("ringOfHealing");

    const useSaphire = checkSaphire.checked;
    // O estado dos rings já está correto aqui graças à handleRingExclusivity()
    const useLifeRing = checkLifeRing.checked; 
    const useRoH = checkRoH.checked;

    if (!runaSelecionada || !vocacaoSelecionada) return;

    const runa = runas[runaSelecionada];
    let regenBase = vocacoes[vocacaoSelecionada];
    let regenTotal = regenBase;
    
    let saphireManaMS = 0;
    let ringManaMS = 0;
    let ringNome = "Nenhum";
    
    let saphireDuracao = 0;
    let ringDuracao = 0;


    // --- 2. CÁLCULO DAS REGENS EXTRAS ---
    
    // A. Giant Saphire Amulet
    if (useSaphire) {
        saphireManaMS = REGEN_BOOSTS.giantSaphire.regen_ms;
        saphireDuracao = REGEN_BOOSTS.giantSaphire.duracao;
    }

    // B. Ring Escolhido (Lógica simplificada após a exclusividade ser garantida no HTML/JS)
    if (useRoH) {
        ringManaMS = REGEN_BOOSTS.ringOfHealing.regen_ms;
        ringDuracao = REGEN_BOOSTS.ringOfHealing.duracao;
        ringNome = REGEN_BOOSTS.ringOfHealing.nome;
    } else if (useLifeRing) {
        ringManaMS = REGEN_BOOSTS.lifeRing.regen_ms;
        ringDuracao = REGEN_BOOSTS.lifeRing.duracao;
        ringNome = REGEN_BOOSTS.lifeRing.nome;
    }

    // C. Acumulação: Soma a regeneração
    regenTotal += saphireManaMS + ringManaMS;


    // --- 3. CÁLCULO DE TEMPO E BP (BACKPACK) ---
    
    // Tempo (segundos) = Mana total / Mana por Segundo Total
    const tempoRunaSeg = runa.mana / regenTotal; 
    const tempoBP = tempoRunaSeg * 20;

    // Exibição do Tempo
    document.getElementById("tempoRuna").textContent = `Tempo para 1 runa: ${formatarTempo(tempoRunaSeg)}`;
    document.getElementById("tempoBP").textContent = `Tempo para 1 backpack (20): ${formatarTempo(tempoBP)}`;


    // --- 4. CÁLCULO DE CONSUMÍVEIS (FOODS) ---
    
    const food = foods[foodSelecionada];
    const foodsNecessarias = Math.ceil(tempoBP / food.duracao);
    
    // Exibição da Food
    document.getElementById("foodBP_quantity").textContent =
        `${foodsNecessarias} ${food.nome}${foodsNecessarias > 1 ? "s" : ""}`;


    // --- 5. CÁLCULO E EXIBIÇÃO DE BOOSTS (AMULETS/RINGS) ---
    
    // A. Giant Saphire
    if (useSaphire) {
        const saphireNecessarios = Math.ceil(tempoBP / saphireDuracao);
        document.getElementById("saphire-info").textContent = 
            `Giant Saphire: ${saphireNecessarios}x (dura total: ${formatarTempo(saphireNecessarios * saphireDuracao)})`;
    } else {
        document.getElementById("saphire-info").textContent = "Giant Saphire: Não utilizado.";
    }

    // B. Ring
    if (useRoH || useLifeRing) {
        const ringNecessarios = Math.ceil(tempoBP / ringDuracao);
        document.getElementById("ring-info").textContent = 
            `${ringNome}: ${ringNecessarios}x (dura total: ${formatarTempo(ringNecessarios * ringDuracao)})`;
    } else {
        document.getElementById("ring-info").textContent = "Ring: Nenhum utilizado.";
    }
}


// =================================================================
// FUNÇÕES DE FORMATAÇÃO E INICIALIZAÇÃO
// =================================================================

function formatarTempo(segundos) {
    const h = Math.floor(segundos / 3600);
    const m = Math.floor((segundos % 3600) / 60);
    const s = Math.floor(segundos % 60);
    return `${h}h ${m}m ${s}s`;
}

function popularRunas() {
    const runaSelect = document.getElementById("runa");
    runaSelect.innerHTML = ""; 

    for (const key in runas) {
        const runa = runas[key];
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = runa.nome;
        runaSelect.appendChild(opt);
    }
}

function popularFoods() {
    const foodSelect = document.getElementById("food");
    foodSelect.innerHTML = ""; 

    for (const key in foods) {
        const food = foods[key];
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = food.nome;
        foodSelect.appendChild(opt);
    }
}

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

    popularFoods();
    calcularTempo();
}


// =================================================================
// INICIALIZAÇÃO E EVENT LISTENERS (NOVOS HANDLERS ADICIONADOS)
// =================================================================

// Listeners de seleção (Existentes)
document.getElementById("runa").addEventListener("change", atualizarRuna);
document.getElementById("vocacao").addEventListener("change", calcularTempo);
document.getElementById("food").addEventListener("change", calcularTempo);

// Listeners para os Checkboxes e a Função de Exclusividade
document.getElementById("giantSaphire").addEventListener("change", calcularTempo);
document.getElementById("lifeRing").addEventListener("change", (e) => handleRingExclusivity(e.target.id)); 
document.getElementById("ringOfHealing").addEventListener("change", (e) => handleRingExclusivity(e.target.id));


popularRunas();
// O call para atualizarRuna() irá chamar popularFoods() e calcularTempo()
atualizarRuna();