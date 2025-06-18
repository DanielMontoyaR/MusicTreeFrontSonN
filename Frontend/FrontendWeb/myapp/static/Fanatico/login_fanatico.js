console.log("Script de login fanatico cargado");

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar/ocultar contraseña mejorado
    const togglePassword = () => {
        const passwordInput = document.getElementById('password');
        const icon = document.getElementById('togglePassword');
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.replace('fa-eye', 'fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.replace('fa-eye-slash', 'fa-eye');
        }
    };
    
    document.getElementById('togglePassword').addEventListener('click', togglePassword);

    // Manejo del formulario de login optimizado
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Elementos del DOM
        const errorElement = document.getElementById('loginError');
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();
        
        // Resetear mensajes
        errorElement.style.display = 'none';
        
        // Validación mejorada
        if (!username || !password) {
            errorElement.textContent = 'Por favor completa todos los campos requeridos';
            errorElement.style.display = 'block';
            return;
        }
        
        try {
            console.log('Intento de login con:', { username, password}); // No registrar contraseña
            
            const response = await fetch('/login_fanatico/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ username, password })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Error en la autenticación');
            }
            
            console.log('Redirigiendo a géneros musicales...');
            window.location.href = '/generos_musicales';
            
        } catch (error) {
            console.error('Error en login:', error);
            errorElement.textContent = error.message || 'Error al conectar con el servidor';
            errorElement.style.display = 'block';
        }
    });
});