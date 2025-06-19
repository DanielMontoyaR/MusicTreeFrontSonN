document.addEventListener('DOMContentLoaded', function() {
    // Mostrar/Ocultar comentarios
    document.getElementById('showCommentsBtn').addEventListener('click', function() {
        const commentsSection = document.getElementById('commentsSection');
        if (commentsSection.style.display === 'none') {
            commentsSection.style.display = 'block';
            this.textContent = 'Ocultar Comentarios';
        } else {
            commentsSection.style.display = 'none';
            this.textContent = 'Cargar Comentarios';
        }
    });

    // Mostrar/Ocultar eventos
    document.getElementById('showEventsBtn').addEventListener('click', function() {
        const eventsSection = document.getElementById('eventsSection');
        if (eventsSection.style.display === 'none') {
            eventsSection.style.display = 'block';
            this.textContent = 'Ocultar Calendario';
        } else {
            eventsSection.style.display = 'none';
            this.textContent = 'Mostrar Calendario de Eventos';
        }
    });
});