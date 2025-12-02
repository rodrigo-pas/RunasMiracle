// O nome do arquivo JSON base de onde extraímos a lista de membros
const GUILD_MEMBER_SOURCE_FILE = 'members_list.json'; 

async function loadGuildMembers() {
    const container = document.getElementById('member-list-container');
    const countElement = document.getElementById('member-count');
    const updateElement = document.getElementById('last-update');
    
    // Adiciona o timestamp para evitar cache do navegador
    const timestamp = new Date().getTime();
    const fileName = `${GUILD_MEMBER_SOURCE_FILE}?v=${timestamp}`;
    
    try {
        const response = await fetch(fileName);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        // --- Constrói a lista HTML (Agora com Nome e Rank) ---
        let listHTML = '<ul class="guild-members-list">';
        
        // Membros são uma lista de objetos: { name: '...', rank: '...' }
        data.members.forEach(member => {
            // Exibe o nome e o cargo/rank
            listHTML += `<li><span class="member-rank">${member.rank}</span> ${member.name}</li>`;
        });
        listHTML += '</ul>';

        // Formatação da Data
        const [datePart, timePart] = data.timestamp.split(' ');
        const formattedDate = datePart.split('-').reverse().join('/'); 
        
        // Atualiza o DOM
        container.innerHTML = listHTML;
        countElement.textContent = `Total de Membros: ${data.total_members}`;
        updateElement.textContent = `Lista atualizada em: ${formattedDate} ${timePart}`;


    } catch (error) {
        container.innerHTML = `<p class="error-message">Erro ao carregar a lista de membros. Verifique se o arquivo JSON foi gerado.</p>`;
        countElement.textContent = `Lista indisponível`;
        updateElement.textContent = `Lista atualizada em: Falha`;
        console.error('Erro:', error);
    }
}

// Inicia o carregamento quando a página está pronta
document.addEventListener('DOMContentLoaded', loadGuildMembers);