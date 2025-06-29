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
        const artistId = new URLSearchParams(window.location.search).get('artist_id');
        const fanId = document.getElementById('fan-id').value;

        if (rating === 0) {
            showAlert('Por favor selecciona una calificación', 'warning');
            return;
        }

        if (!artistId || !fanId) {
            showAlert('Error: No se pudo identificar al artista o al fanático', 'danger');
            return;
        }

        try {
            // Mostrar spinner o indicador de carga
            submitRatingBtn.disabled = true;
            submitRatingBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';

            // Llamada a través de Django
            const response = await fetch('/rate_artist/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    artist_id: artistId,
                    rating: rating
                    // fan_id lo obtenemos de la sesión en el backend
                })
            });

            const data = await response.json();

            if (!response.ok) {
                if (response.status === 200 && data.error && data.error.includes("ya calificó")) {
                    showAlert(data.error, 'warning');
                } else {
                    throw new Error(data.error || 'Error al enviar la calificación');
                }
            } else {
                showAlert(data.message || '¡Gracias por tu calificación!', 'success');
                updateMainRatingStars(rating);

                // Recargar la página después de 1.5 segundos
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }

        } catch (error) {
            showAlert(error.message, 'danger');
        } finally {
            submitRatingBtn.disabled = false;
            submitRatingBtn.textContent = 'Enviar Calificación';
        }
    });

    // Función para obtener cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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