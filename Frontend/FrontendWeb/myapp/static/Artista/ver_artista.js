document.addEventListener('DOMContentLoaded', function () {
    // Lógica para el sistema de calificación
    const ratingStars = document.querySelectorAll('.rating-star');
    const selectedRatingInput = document.getElementById('selectedRating');
    const submitRatingBtn = document.getElementById('submitRating');
    const mainRatingStars = document.querySelectorAll('.rating-stars .fa-star, .rating-stars .fa-regular');
    let currentRating = 0;
    let hoverRating = 0;

    // Función para actualizar las estrellas principales
    function updateMainRatingStars(rating) {
        mainRatingStars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('fa-regular');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('fa-regular');
            }
        });
    }

    // Manejar hover sobre estrellas
    ratingStars.forEach(star => {
        star.addEventListener('mouseover', function () {
            const value = parseInt(this.getAttribute('data-value'));
            hoverRating = value;
            highlightStars(value);
        });

        star.addEventListener('mouseout', function () {
            highlightStars(currentRating);
        });

        star.addEventListener('click', function () {
            const value = parseInt(this.getAttribute('data-value'));
            currentRating = value;
            selectedRatingInput.value = value;
            highlightStars(value);
        });
    });

submitRatingBtn.addEventListener('click', async function () {
    const rating = parseInt(selectedRatingInput.value);

    if (rating === 0) {
        showAlert('Por favor selecciona una calificación', 'warning');
        return;
    }

    try {
        // Mostrar spinner o indicador de carga
        submitRatingBtn.disabled = true;
        submitRatingBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';

        // Simular llamada a API (reemplazar con fetch real)
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Mostrar mensaje de éxito
        showAlert('¡Gracias por tu calificación!', 'success');

        // Recargar la página después de 1.5 segundos
        setTimeout(() => {
            window.location.reload();
        }, 1500);

    } catch (error) {
        showAlert('Error al enviar la calificación', 'danger');
        submitRatingBtn.disabled = false;
        submitRatingBtn.textContent = 'Enviar Calificación';
    }
});

    // Función para mostrar alertas elegantes
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
        alertDiv.style.zIndex = '1100';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-eliminar después de 3 segundos
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }

    // Función para resaltar estrellas en el modal
    function highlightStars(count) {
        ratingStars.forEach(star => {
            const value = parseInt(star.getAttribute('data-value'));
            star.classList.remove('fa-solid', 'fa-regular', 'selected', 'hovered');
            
            if (value <= count) {
                star.classList.add(count === hoverRating ? 'hovered' : 'selected');
                star.classList.add('fa-solid');
            } else {
                star.classList.add('fa-regular');
            }
        });
    }
});