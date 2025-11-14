// SKILLS utilizadas no python (dicionário)
const SKILLS_MAP = {
    'experience': 'Level',
    'sword': 'Sword',
    'axe': 'Axe',
    'club': 'Club',
    'dist': 'Distance',
    'maglevel': 'Magic Level',
    'shielding': 'Shielding',
    'fishing': 'Fishing',
    'mage_skill': 'Mage Skills' 
};

// 1. Cria os botões de skill no HTML
function createSkillButtons() {
    const selectorDiv = document.getElementById('skill-selectors');
    if (!selectorDiv) return;
    
    selectorDiv.innerHTML = ''; // Limpa antes de popular
    let firstButtonKey = null;

    for (const key in SKILLS_MAP) {
        if (!firstButtonKey) {
            firstButtonKey = key;
        }
        const button = document.createElement('button');
        button.textContent = SKILLS_MAP[key];
        button.className = 'skill-button';
        button.setAttribute('data-skill-key', key); // Usado para referenciar o botão no loadRanking
        
        // CORREÇÃO: Passa a referência do botão e usa event.currentTarget para o clique
        button.onclick = (event) => loadRanking(key, event.currentTarget); 
        
        selectorDiv.appendChild(button);
    }
}

// 2. Carrega o arquivo JSON e exibe o ranking
async function loadRanking(skillKey, clickedButton) {
    const resultsDiv = document.getElementById('ranking-results');
    const updateTimeElement = document.getElementById('last-update');
    const titleElement = document.getElementById('current-skill-title');
    
    // Altera o estado visual dos botões
    document.querySelectorAll('.skill-button').forEach(btn => btn.classList.remove('active'));
    if (clickedButton) {
        clickedButton.classList.add('active');
    }

    titleElement.textContent = `Carregando Ranking de ${SKILLS_MAP[skillKey]}...`;
    resultsDiv.innerHTML = '<p>Buscando dados...</p>';
    updateTimeElement.textContent = 'Última atualização: Carregando...';

    // --- CORREÇÃO DE CACHE: Adiciona o timestamp para forçar a atualização ---
    const timestamp = new Date().getTime();
    const fileName = `ranking_${skillKey}.json?v=${timestamp}`;
    // --- FIM DA CORREÇÃO DE CACHE ---
    
    try {
        const response = await fetch(fileName);
        
        if (!response.ok) {
            // Se der erro 404, o arquivo não existe ou a chave do JSON está errada
            throw new Error(`Erro HTTP! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        displayRanking(data);

    } catch (error) {
        resultsDiv.innerHTML = `<p class="error-message">Erro ao carregar o ranking. O arquivo "${fileName.split('?')[0]}" pode não existir ou a rede falhou.</p>`;
        updateTimeElement.textContent = `Última atualização: Falha!`;
        console.error('Erro ao carregar ranking:', error);
    }
}

// 3. Renderiza a tabela no HTML
function displayRanking(data) {
    const resultsDiv = document.getElementById('ranking-results');
    const titleElement = document.getElementById('current-skill-title');
    const updateTimeElement = document.getElementById('last-update');
    
    titleElement.textContent = `TOP ${data.value_type} - ${data.skill_name}`;
    
    // --- FORMATAÇÃO DA DATA PARA DD/MM/YYYY ---
    const timestamp = data.timestamp; 
    const [datePart, timePart] = timestamp.split(' ');
    const formattedDate = datePart.split('-').reverse().join('/'); 
    const formattedTimestamp = `${formattedDate} ${timePart}`; 

    updateTimeElement.textContent = `Última atualização: ${formattedTimestamp}`;
    // --- FIM DA FORMATAÇÃO DA DATA ---
    
    if (data.ranking.length === 0) {
        resultsDiv.innerHTML = `<p>Nenhum membro da guilda encontrado no ranking global de ${data.skill_name}.</p>`;
        return;
    }

    let tableHTML = `
        <table class="ranking-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Nome</th>
                    <th>${data.value_type}</th>
                </tr>
            </thead>
            <tbody>
    `;

    data.ranking.forEach(member => {
        tableHTML += `
            <tr>
                <td>${member.rank_guild}</td>
                <td>${member.nome}</td>
                <td>${member.valor}</td>
            </tr>
        `;
    });

    tableHTML += `
            </tbody>
        </table>
    `;

    resultsDiv.innerHTML = tableHTML;
}

// Inicialização: Cria os botões quando a página carrega
document.addEventListener('DOMContentLoaded', createSkillButtons);

// Carrega o ranking de Experience por padrão na primeira carga
document.addEventListener('DOMContentLoaded', () => {
    // Adiciona um pequeno delay para garantir que os botões sejam criados
    setTimeout(() => {
        // Encontra o botão de 'experience' pelo atributo data-skill-key
        const experienceButton = document.querySelector('[data-skill-key="experience"]');
        if (experienceButton) {
            experienceButton.click();
        }
    }, 100); 
});