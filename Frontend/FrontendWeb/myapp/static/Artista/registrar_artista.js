console.log("Script de registro de artista cargado!");
document.addEventListener('DOMContentLoaded', async function () {
    // Variables para contar grupos
    let MemberCount = 0;
    let albumCount = 0;
    let generoCount = 0;
    let subgeneroCount = 0;

    // Vista previa de la portada
    document.getElementById('portada').addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const preview = document.getElementById('portadaPreview');
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Validación del nombre
    document.getElementById('nombre').addEventListener('input', function () {
        this.classList.toggle('is-invalid', this.value.length < 3 || this.value.length > 100);
    });

    // Llenar países
    // Llenar países de la ONU (lista simplificada)
    const { paisesONU } = await import("../GeneralData/paises.js");


    const paisSelect = document.getElementById('pais');
    paisesONU.sort().forEach(pais => {
        const option = document.createElement('option');
        option.value = pais;
        option.textContent = pais;
        paisSelect.appendChild(option);
    });


    // Llenar años desde (1850-2025)
    const yearSelect_desde = document.getElementById('anio_desde');
    const currentYear = new Date().getFullYear();
    for (let year = 1850; year <= 2025; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        // Seleccionar el año actual por defecto
        if (year === currentYear) option.selected = true;
        yearSelect_desde.appendChild(option);
    }


    // Llenar años hasta (1850-2025)
    const yearSelect_hasta = document.getElementById('anio_hasta');
    for (let year = 1850; year <= 2025; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        // Seleccionar el año actual por defecto
        //if (year === currentYear) option.selected = true;
        yearSelect_hasta.appendChild(option);
    }

    // Validación años de actividad
    document.getElementById('anio_hasta').addEventListener('change', function () {
        const desde = parseInt(document.getElementById('anio_desde').value);
        const hasta = this.value === 'presente' ? new Date().getFullYear() : parseInt(this.value);

        if (desde > hasta) {
            document.getElementById('anio_desde').classList.add('is-invalid');
            this.classList.add('is-invalid');
        } else {
            document.getElementById('anio_desde').classList.remove('is-invalid');
            this.classList.remove('is-invalid');
        }
    });


    //Asociar género
    document.getElementById('addGenero').addEventListener('click', function () {
        generoCount++;
        const html = `
        <div class="genero-group mb-3 p-3 border rounded" id="genero${generoCount}">
            <div class="mb-3">
                <label for="generoSelect${generoCount}" class="form-label">Género ${generoCount}*</label>
                <select class="form-select genero-select" id="generoSelect${generoCount}" 
                        name="generos[]" required>
                    <option value="" selected disabled>Seleccione un género...</option>
                    <!-- Géneros se cargarán dinámicamente -->
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
                    option.value = genero.id; // Usar genre_id en lugar de id
                    option.textContent = genero.nombre;
                    select.setAttribute('data-genre-name', genero.nombre); // Guardar el nombre como atributo
                    select.appendChild(option);
                });
            } catch (error) {
                console.error('Error:', error);
                alert('Error al cargar géneros');
            }
        }
        // Llama la función para cargar géneros en el select recién creado
        cargarGenerosPrincipalesEnSelect(`generoSelect${generoCount}`);


    });

    // Función para quitar género
    document.getElementById('removeGenero').addEventListener('click', function () {
        if (generoCount > 0) {
            document.getElementById(`genero${generoCount}`).remove();
            generoCount--;
        }
    });


    // Función para agregar subgénero
    document.getElementById('addSubgenero').addEventListener('click', function () {
        subgeneroCount++;
        const html = `
        <div class="subgenero-group mb-3 p-3 border rounded" id="subgenero${subgeneroCount}">
            <div class="mb-3">
                <label for="subgeneroSelect${subgeneroCount}" class="form-label">Subgénero ${subgeneroCount}</label>
                <select class="form-select subgenero-select" id="subgeneroSelect${subgeneroCount}" 
                        name="subgeneros[]">
                    <option value="" selected disabled>Seleccione un subgénero...</option>
                    <!-- Subgéneros se cargarán dinámicamente -->
                </select>
            </div>
        </div>
    `;
        document.getElementById('subgenerosContainer').insertAdjacentHTML('beforeend', html);

        // Función para cargar géneros desde Django
        async function cargarSubGenerosPrincipalesEnSelect(selectId) {
            try {
                const response = await fetch('/api/subgenres/');
                if (!response.ok) throw new Error('Error al cargar géneros');

                const subgeneros = await response.json();
                const select = document.getElementById(selectId);

                // Limpiar y poblar el select
                select.innerHTML = '<option value="" selected disabled>Seleccione un género...</option>';
                subgeneros.forEach(subgenero => {
                    const option = document.createElement('option');
                    option.value = subgenero.id; // Usar genre_id en lugar de id
                    option.textContent = subgenero.nombre;
                    select.setAttribute('data-genre-name', subgenero.nombre); // Guardar el nombre como atributo
                    select.appendChild(option);
                });
            } catch (error) {
                console.error('Error:', error);
                alert('Error al cargar géneros');
            }
        }

        cargarSubGenerosPrincipalesEnSelect(`subgeneroSelect${subgeneroCount}`);

    });

    // Función para quitar subgénero
    document.getElementById('removeSubgenero').addEventListener('click', function () {
        if (subgeneroCount > 0) {
            document.getElementById(`subgenero${subgeneroCount}`).remove();
            subgeneroCount--;
        }
    });


    // Agregar miembro antiguo
    document.getElementById('addMember').addEventListener('click', function () {
        MemberCount++;
        const html = `
            <div class="member-group" id="Member${MemberCount}">
                <h5>Miembro ${MemberCount}</h5>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="MemberName${MemberCount}" class="form-label">Nombre*</label>
                        <input type="text" class="form-control" id="MemberName${MemberCount}" 
                               name="MemberName${MemberCount}" required>
                    </div>
                    <div class="col-md-4">
                        <label for="MemberInstrument${MemberCount}" class="form-label">Instrumento*</label>
                        <input type="text" class="form-control" id="MemberInstrument${MemberCount}" 
                               name="MemberInstrument${MemberCount}" required>
                    </div>
                    <div class="col-md-2">
                        <label for="MemberSince${MemberCount}" class="form-label">Desde*</label>
                        <select class="form-select" id="MemberSince${MemberCount}" 
                                name="MemberSince${MemberCount}" required>
                            <option value="" selected disabled>Seleccione un año</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                    <div class="col-md-2">
                        <label for="MemberUntil${MemberCount}" class="form-label">Hasta*</label>
                        <select class="form-select" id="MemberUntil${MemberCount}" 
                                name="MemberUntil${MemberCount}" required>
                            <option value="presente">Presente</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('MembersContainer').insertAdjacentHTML('beforeend', html);
        // Llenar el select de años
        const select_since = document.getElementById(`MemberSince${MemberCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select_since.appendChild(option);
        }

        // Llenar el select de años
        const select_until = document.getElementById(`MemberUntil${MemberCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select_until.appendChild(option);
        }
    });

    // Quitar último miembro antiguo
    document.getElementById('removeMember').addEventListener('click', function () {
        if (MemberCount > 0) {
            document.getElementById(`Member${MemberCount}`).remove();
            MemberCount--;
        }
    });


    document.getElementById('es_banda').addEventListener('change', function () {
        const membersSection = document.getElementById('MembersContainer').parentElement;

        if (MemberCount > 0) {
            for (let i = 0; i < MemberCount; MemberCount--) {
                document.getElementById(`Member${MemberCount}`).remove();
            }

        }
        membersSection.style.display = this.checked ? 'block' : 'none';

    });

    // Agregar álbum
    document.getElementById('addAlbum').addEventListener('click', function () {
        albumCount++;
        const html = `
        <div class="album-group mb-4 p-3 border rounded" id="album${albumCount}">
            <h5 class="mb-3">Álbum ${albumCount}</h5>
            
            <div class="mb-3">
                <label for="albumName${albumCount}" class="form-label">Nombre del Álbum*</label>
                <input type="text" class="form-control" id="albumName${albumCount}" 
                       name="albumName${albumCount}" required>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="albumYear${albumCount}" class="form-label">Año*</label>
                    <select class="form-select" id="albumYear${albumCount}" 
                            name="albumYear${albumCount}" required>
                        <option value="" selected disabled>Seleccione un año</option>
                    </select>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="albumDuration${albumCount}" class="form-label">Duración (min)*</label>
                    <input type="number" class="form-control" id="albumDuration${albumCount}" 
                           name="albumDuration${albumCount}" min="1" step="1" required>
                </div>
            </div>
            
            <div class="mb-3">
                <label for="albumImage${albumCount}" class="form-label">Imagen del Álbum</label>
                <input type="file" class="form-control" id="albumImage${albumCount}" 
                       name="albumImage${albumCount}" accept="image/jpeg">
                <div class="form-text">JPEG, relación 1:1, máximo 5MB</div>
                <img id="albumPreview${albumCount}" class="img-thumbnail mt-2 album-preview" 
                     style="display: none; max-width: 200px; max-height: 200px;">
            </div>
        </div>
    `;
        document.getElementById('albumsContainer').insertAdjacentHTML('beforeend', html);


        // Llenar el select de años
        const select_year = document.getElementById(`albumYear${albumCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select_year.appendChild(option);
        }

        // Agregar evento para previsualización
        document.getElementById(`albumImage${albumCount}`).addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    const preview = document.getElementById(`albumPreview${albumCount}`);
                    preview.src = event.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Quitar último álbum
    document.getElementById('removeAlbum').addEventListener('click', function () {
        if (albumCount > 0) {
            document.getElementById(`album${albumCount}`).remove();
            albumCount--;
        }
    });

    // Inicializar con un miembro actual
    document.getElementById('addMember').click();



    // 3. Función para mostrar datos en console.log al enviar
    document.getElementById('artistForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    // Validaciones (las que ya tenías)
    let isValid = true;
    if (generoCount === 0) {
        document.getElementById('generoError').style.display = 'block';
        isValid = false;
    } else {
        document.getElementById('generoError').style.display = 'none';
    }

    const portada = document.getElementById('portada').files[0];
    if (!portada) {
        alert('Debes seleccionar una imagen de portada');
        isValid = false;
    }

    if (albumCount === 0) {
        alert('Debes agregar al menos un álbum');
        isValid = false;
    }

    if (!isValid) return;

    try {
        // 1. Crear FormData para enviar archivos y datos
        const formData = new FormData();

        // 2. Agregar campos básicos
        formData.append('es_banda', document.getElementById('es_banda').checked);
        formData.append('nombre', document.getElementById('nombre').value);
        formData.append('biografia', document.getElementById('biografia').value);
        formData.append('pais', document.getElementById('pais').value);
        formData.append('anio_desde', document.getElementById('anio_desde').value);
        formData.append('anio_hasta', document.getElementById('anio_hasta').value);
        formData.append('portada', portada);

        // 3. Agregar géneros (como array)
        for (let i = 1; i <= generoCount; i++) {
            const generoSelect = document.getElementById(`generoSelect${i}`);
            if (generoSelect && generoSelect.value) {
                formData.append('generos[]', generoSelect.value);
            }
        }

        // 4. Agregar subgéneros (como array)
        for (let i = 1; i <= subgeneroCount; i++) {
            const subgeneroSelect = document.getElementById(`subgeneroSelect${i}`);
            if (subgeneroSelect && subgeneroSelect.value) {
                formData.append('subgeneros[]', subgeneroSelect.value);
            }
        }

        // 5. Agregar miembros
        for (let i = 1; i <= MemberCount; i++) {
            if (document.getElementById(`Member${i}`)) {
                formData.append(`MemberName${i}`, document.getElementById(`MemberName${i}`).value);
                formData.append(`MemberInstrument${i}`, document.getElementById(`MemberInstrument${i}`).value);
                formData.append(`MemberSince${i}`, document.getElementById(`MemberSince${i}`).value);
                formData.append(`MemberUntil${i}`, document.getElementById(`MemberUntil${i}`).value);
            }
        }

        // 6. Agregar álbumes
        for (let i = 1; i <= albumCount; i++) {
            if (document.getElementById(`album${i}`)) {
                formData.append(`albumName${i}`, document.getElementById(`albumName${i}`).value);
                formData.append(`albumYear${i}`, document.getElementById(`albumYear${i}`).value);
                formData.append(`albumDuration${i}`, document.getElementById(`albumDuration${i}`).value);
                
                const albumImage = document.getElementById(`albumImage${i}`).files[0];
                if (albumImage) {
                    formData.append(`albumImage${i}`, albumImage);
                }
            }
        }

        // 7. Enviar al backend Django
        const response = await fetch('/registrar_artista/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });

        // 8. Manejar respuesta
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Error en el servidor');
        }

        const result = await response.json();
        
        if (result.success) {
            alert('Artista registrado exitosamente!');
            // Redirigir o limpiar formulario
            window.location.href = '/ver_artista'; // Ajusta la ruta según necesites
        } else {
            alert(result.message || 'Error al registrar artista');
        }

    } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Ocurrió un error al enviar el formulario');
        
        // Mostrar error en la interfaz si es necesario
        const errorElement = document.getElementById('formError');
        if (errorElement) {
            errorElement.textContent = error.message;
            errorElement.style.display = 'block';
        }
    }
});
});
