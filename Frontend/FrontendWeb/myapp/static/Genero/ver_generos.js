console.log("Script de ver generos cargado!")
document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const genreCards = document.querySelectorAll('.genre-card');
    
    // Función para filtrar géneros
    function filterGenres() {
        const searchTerm = searchInput.value.trim().toLowerCase();
        
        genreCards.forEach(card => {
            const genreName = card.querySelector('.genre-name').textContent.toLowerCase();
            const genreId = card.querySelector('.genre-id').textContent.toLowerCase();
            
            // Mostrar/ocultar según coincidencia
            if (genreName.includes(searchTerm) || genreId.includes(searchTerm)) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    }
    
    // Event listeners
    searchInput.addEventListener('input', filterGenres);
    searchBtn.addEventListener('click', filterGenres);
    
    // Opcional: Focus automático en el buscador
    searchInput.focus();
    
    // Opcional: Mostrar mensaje si no hay coincidencias
    function checkNoResults() {
        const visibleCards = document.querySelectorAll('.genre-card:not(.hidden)');
        const noResultsMsg = document.querySelector('.no-results-message');
        
        if (visibleCards.length === 0 && searchInput.value.trim() !== '') {
            if (!noResultsMsg) {
                const msg = document.createElement('div');
                msg.className = 'alert alert-warning text-center no-results-message';
                msg.innerHTML = '<i class="fas fa-search"></i> No se encontraron géneros que coincidan';
                document.getElementById('genresList').appendChild(msg);
            }
        } else if (noResultsMsg) {
            noResultsMsg.remove();
        }
    }
    
    // Ejecutar checkNoResults cuando se filtre
    searchInput.addEventListener('input', checkNoResults);
    searchBtn.addEventListener('click', checkNoResults);
});