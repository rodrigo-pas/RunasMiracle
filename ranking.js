// Os nomes das SKILLS devem ser os mesmos que você usou no Python (as chaves do dicionário)
const SKILLS_MAP = {
    'experience': 'Level / Exp',
    'sword': 'Sword',
    'axe': 'Axe',
    'club': 'Club',
    'dist': 'Distance',
    'maglevel': 'Magic Level',
    'shielding': 'Shielding',
    'fishing': 'Fishing',
};

// 1. Cria os botões de skill no HTML
function createSkillButtons() {
    const selectorDiv = document.getElementById('skill-selectors');
    selectorDiv.innerHTML = ''; // Limpa antes de popular

    for (const key in SKILLS_MAP) {
        const button = document.createElement('button');
        button.textContent = SKILLS_MAP[key];
        button.className = 'skill-button';
        button.onclick = () => loadRanking(key); // Chama a função com a chave da skill (ex: 'sword')
        selectorDiv.appendChild(button);
    }
}

// 2. Carrega o arquivo JSON e exibe o ranking
async function loadRanking(skillKey) {
    const resultsDiv = document.getElementById('ranking-results');
    const updateTimeElement = document.getElementById('last-update');
    const titleElement = document.getElementById('current-skill-title');
    
    // Altera o estado visual dos botões
    document.querySelectorAll('.skill-button').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active'); 

    titleElement.textContent = `Carregando Ranking de ${SKILLS_MAP[skillKey]}...`;
    resultsDiv.innerHTML = '<p>Buscando dados...</p>';
    updateTimeElement.textContent = 'Última atualização: Carregando...';

    const fileName = `ranking_${skillKey}.json`;
    
    try {
        // Faz a requisição para o arquivo JSON (fetch)
        const response = await fetch(fileName);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Se a requisição for bem-sucedida, gera a tabela
        displayRanking(data);

    } catch (error) {
        resultsDiv.innerHTML = `<p class="error-message">Erro ao carregar o arquivo ${fileName}. Certifique-se de que ele foi gerado e enviado para o GitHub.</p>`;
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
    
    // --- CORREÇÃO DA DATA PARA O PADRÃO BRASILEIRO ---
    const timestamp = data.timestamp; // Ex: "2025-11-03 12:00:00"
    
    // Divide o timestamp em Data e Hora
    const [datePart, timePart] = timestamp.split(' ');
    
    // Reverte a ordem da data de YYYY-MM-DD para DD/MM/YYYY
    const formattedDate = datePart.split('-').reverse().join('/'); 
    
    // Junta a nova data com a hora
    const formattedTimestamp = `${formattedDate} ${timePart}`; 

    updateTimeElement.textContent = `Última atualização: ${formattedTimestamp}`;
    // --- FIM DA CORREÇÃO DA DATA ---
    
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

// Opcional: Carrega o ranking de Experience por padrão na primeira carga
document.addEventListener('DOMContentLoaded', () => {
    // Adiciona um pequeno delay para garantir que os botões sejam criados antes de tentar o clique
    setTimeout(() => {
        const experienceButton = document.querySelector('.skill-button');
        if (experienceButton) {
            experienceButton.click();
        }
    }, 100); 
});