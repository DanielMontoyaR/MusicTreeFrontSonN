console.log("Script de registro de fanatico cargado!!");
//import { paisesONU } from "../GeneralData/paises";  

document.addEventListener('DOMContentLoaded',async function () {
    
    
    // Variables para contar géneros seleccionados
    let generoCount = 0;
    let selectedAvatar = null;

    // Mostrar/ocultar contraseña
    document.getElementById('togglePassword').addEventListener('click', function () {
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

    // Validación del nombre de usuario
    document.getElementById('username').addEventListener('input', function () {
        this.classList.toggle('is-invalid', this.value.length > 30);
    });

    // Validación de la contraseña
    document.getElementById('password').addEventListener('input', function () {
        const password = this.value;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const isValid = password.length >= 8 &&
            password.length <= 12 &&
            hasUpperCase &&
            hasLowerCase &&
            hasNumbers;

        this.classList.toggle('is-invalid', !isValid);
    });

    // Validación del nombre completo
    document.getElementById('fullname').addEventListener('input', function () {
        this.classList.toggle('is-invalid', this.value.length > 100);
    });

    const { paisesONU } = await import("../GeneralData/paises.js");
    // Llenar países (simplificado)
    const paisSelect = document.getElementById('pais');
    paisesONU.sort().forEach(pais => {
        const option = document.createElement('option');
        option.value = pais;
        option.textContent = pais;
        paisSelect.appendChild(option);
    });

    // Selección de avatar
    document.querySelectorAll('.avatar-option').forEach(avatar => {
        avatar.addEventListener('click', function () {
            // Remover selección anterior
            document.querySelectorAll('.avatar-option').forEach(a => {
                a.classList.remove('selected');
            });

            // Marcar como seleccionado
            this.classList.add('selected');
            selectedAvatar = this.getAttribute('data-avatar');
            document.getElementById('selectedAvatar').value = selectedAvatar;
            document.getElementById('avatarError').style.display = 'none';
        });
    });

    // Agregar género
    document.getElementById('addGenero').addEventListener('click', function () {
        generoCount++;
        const html = `
            <div class="genero-group mb-3 p-3 border rounded" id="genero${generoCount}">
                <div class="mb-3">
                    <label for="generoSelect${generoCount}" class="form-label">Género ${generoCount}*</label>
                    <select class="form-select genero-select" id="generoSelect${generoCount}" 
                            name="generos[]" required>
                        <option value="" selected disabled>Seleccione un género...</option>
                    </select>
                </div>
            </div>
        `;
        document.getElementById('generosContainer').insertAdjacentHTML('beforeend', html);

        // Función para cargar géneros desde Django
        async function cargarGenerosPrincipalesEnSelect(selectId) {
            try {
                const response = await fetch('/api/genres/');
                if (!response.ok) throw new Error('Error al cargar géneros');

                const generos = await response.json();
                const select = document.getElementById(selectId);

                // Limpiar y poblar el select
                select.innerHTML = '<option value="" selected disabled>Seleccione un género...</option>';
                generos.forEach(genero => {
                    const option = document.createElement('option');
                    option.value = genero.id;
                    option.textContent = genero.nombre;
                    select.appendChild(option);
                });
            } catch (error) {
                console.error('Error:', error);
                alert('Error al cargar géneros');
            }
        }

        // Cargar géneros en el select recién creado
        cargarGenerosPrincipalesEnSelect(`generoSelect${generoCount}`);
    });

    // Quitar último género
    document.getElementById('removeGenero').addEventListener('click', function () {
        if (generoCount > 0) {
            document.getElementById(`genero${generoCount}`).remove();
            generoCount--;
        }
    });

    // Validación del formulario antes de enviar
    document.getElementById('userForm').addEventListener('submit', async function (e) {
        e.preventDefault();

        // Resetear mensajes
        document.getElementById('successMessage').style.display = 'none';
        document.getElementById('errorMessage').style.display = 'none';

        // Validaciones
        let isValid = true;

        // Validar nombre de usuario
        const username = document.getElementById('username').value;
        if (username.length > 30 || username.length === 0) {
            document.getElementById('username').classList.add('is-invalid');
            isValid = false;
        }

        // Validar contraseña
        const password = document.getElementById('password').value;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        if (password.length < 8 || password.length > 12 || !hasUpperCase || !hasLowerCase || !hasNumbers) {
            document.getElementById('password').classList.add('is-invalid');
            isValid = false;
        }

        // Validar nombre completo
        const fullname = document.getElementById('fullname').value;
        if (fullname.length > 100 || fullname.length === 0) {
            document.getElementById('fullname').classList.add('is-invalid');
            isValid = false;
        }

        // Validar géneros
        if (generoCount === 0) {
            document.getElementById('generoError').style.display = 'block';
            isValid = false;
        } else {
            // Verificar que todos los géneros tengan selección
            for (let i = 1; i <= generoCount; i++) {
                const generoSelect = document.getElementById(`generoSelect${i}`);
                if (!generoSelect || generoSelect.value === "") {
                    document.getElementById('generoError').style.display = 'block';
                    isValid = false;
                    break;
                }
            }
        }

        // Validar país
        const pais = document.getElementById('pais').value;
        if (!pais) {
            document.getElementById('pais').classList.add('is-invalid');
            isValid = false;
        }

        // Validar avatar
        if (!selectedAvatar) {
            document.getElementById('avatarError').style.display = 'block';
            isValid = false;
        }

        if (!isValid) {
            document.getElementById('errorMessage').textContent = 'Por favor completa todos los campos requeridos correctamente.';
            document.getElementById('errorMessage').style.display = 'block';
            return;
        }

        try {
            const formData = new FormData(this);

            // Crear objeto con los datos del formulario
            const formDataObj = {
                username: formData.get('username'),
                password: '******', // Ocultamos la contraseña por seguridad
                fullname: formData.get('fullname'),
                pais: formData.get('pais'),
                avatar: formData.get('avatar')
            };

            // Procesar géneros (solo los valores sin las llaves)
            const generosValues = [];
            for (let i = 1; i <= generoCount; i++) {
                const generoSelect = document.getElementById(`generoSelect${i}`);
                if (generoSelect && generoSelect.value) {
                    generosValues.push(generoSelect.value);
                }
            }
            formDataObj.generos = generosValues;

            // Mostrar en consola
            console.log("Datos a enviar:", formDataObj);

            // 3. Enviar al backend Django
            const response = await fetch('/registrar_fanatico/', {
                method: 'POST',
                body: formData, // Enviamos FormData directamente
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });

            // 4. Manejar respuesta
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error en el servidor');
            }

            const result = await response.json();

            if (result.success) {
                document.getElementById('successMessage').textContent = result.message;
                document.getElementById('successMessage').style.display = 'block';
                console.log("REDIRIGIENDO A login_fanatico")
                // Redirigir después de 2 segundos
                setTimeout(() => {
                    window.location.href = '/login_fanatico';
                }, 2000);
            } else {
                throw new Error(result.message || 'Error al registrar usuario');
            }

        } catch (error) {
            console.error('Error:', error);
            document.getElementById('errorMessage').textContent = error.message;
            document.getElementById('errorMessage').style.display = 'block';
        }
    });

    // Inicializar con un género por defecto
    document.getElementById('addGenero').click();
});