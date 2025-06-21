console.log("Script de home cargado");

document.addEventListener('DOMContentLoaded', function() {
    // Mostrar/ocultar contraseña
    document.getElementById('togglePassword').addEventListener('click', function() {
        const passwordInput = document.getElementById('password');
        const icon = this;
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            passwordInput.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    });

    // Manejo del formulario de login
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Resetear mensajes de error
        document.getElementById('loginError').style.display = 'none';
        
        // Validar campos
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        if (!username || !password) {
            document.getElementById('loginError').textContent = 'Por favor completa todos los campos requeridos';
            document.getElementById('loginError').style.display = 'block';
            return;
        }
        
        try {
            // Imprimir credenciales en consola (solo para desarrollo)
            console.log('Credenciales ingresadas:', { username, password });
            
            // Crear objeto con los datos del login
            const loginData = {
                username: username,
                password: password
            };
            
            // Enviar al backend Django
            const response = await fetch('/home/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(loginData)
            });
            
            // Procesar respuesta
            const result = await response.json();
            
            if (response.ok && result.success) {
                console.log('Login exitoso. Redirigiendo...');
                window.location.href = '/generos_musicales';
            } else {
                throw new Error(result.error || 'Credenciales incorrectas');
            }
        } catch (error) {
            console.error('Error en login:', error);
            document.getElementById('loginError').textContent = error.message;
            document.getElementById('loginError').style.display = 'block';
        }
    });
});