console.log("Script de registro de artista cargado!");
document.addEventListener('DOMContentLoaded', function() {
    // Variables para contar grupos
    let currentMemberCount = 0;
    let formerMemberCount = 0;
    let albumCount = 0;
    
    // Vista previa de la portada
    document.getElementById('portada').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                const preview = document.getElementById('portadaPreview');
                preview.src = event.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
    
    // Validación del nombre
    document.getElementById('nombre').addEventListener('input', function() {
        this.classList.toggle('is-invalid', this.value.length < 3 || this.value.length > 100);
    });

    // Llenar países
    // Llenar países de la ONU (lista simplificada)
    const paisesONU = [
        "Afganistán", "Albania", "Alemania", "Andorra", "Angola",
        "Antigua y Barbuda", "Arabia Saudita", "Argelia", "Argentina",
        "Armenia", "Australia", "Austria", "Azerbaiyán", "Bahamas",
        "Bangladés", "Barbados", "Baréin", "Bélgica", "Belice",
        "Benín", "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina",
        "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso",
        "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún",
        "Canadá", "Catar", "Chad", "Chile", "China",
        "Chipre", "Colombia", "Comoras", "Corea del Norte", "Corea del Sur",
        "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Dinamarca",
        "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos Árabes Unidos",
        "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos",
        "Estonia", "Esuatini", "Etiopía", "Filipinas", "Finlandia",
        "Fiyi", "Francia", "Gabón", "Gambia", "Georgia",
        "Ghana", "Granada", "Grecia", "Guatemala", "Guinea",
        "Guinea-Bisáu", "Guinea Ecuatorial", "Guyana", "Haití", "Honduras",
        "Hungría", "India", "Indonesia", "Irak", "Irán",
        "Irlanda", "Islandia", "Islas Marshall", "Islas Salomón", "Israel",
        "Italia", "Jamaica", "Japón", "Jordania", "Kazajistán",
        "Kenia", "Kirguistán", "Kiribati", "Kuwait", "Laos",
        "Lesoto", "Letonia", "Líbano", "Liberia", "Libia",
        "Liechtenstein", "Lituania", "Luxemburgo", "Macedonia del Norte", "Madagascar",
        "Malasia", "Malaui", "Maldivas", "Malí", "Malta",
        "Marruecos", "Mauricio", "Mauritania", "México", "Micronesia",
        "Moldavia", "Mónaco", "Mongolia", "Montenegro", "Mozambique",
        "Namibia", "Nauru", "Nepal", "Nicaragua", "Níger",
        "Nigeria", "Noruega", "Nueva Zelanda", "Omán", "Países Bajos",
        "Pakistán", "Palaos", "Panamá", "Papúa Nueva Guinea", "Paraguay",
        "Perú", "Polonia", "Portugal", "Reino Unido", "República Centroafricana",
        "República Checa", "República del Congo", "República Democrática del Congo", "República Dominicana", "Ruanda",
        "Rumanía", "Rusia", "Samoa", "San Cristóbal y Nieves", "San Marino",
        "San Vicente y las Granadinas", "Santa Lucía", "Santo Tomé y Príncipe", "Senegal", "Serbia",
        "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia",
        "Sri Lanka", "Sudáfrica", "Sudán", "Sudán del Sur", "Suecia",
        "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistán",
        "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", "Túnez",
        "Turkmenistán", "Turquía", "Tuvalu", "Ucrania", "Uganda",
        "Uruguay", "Uzbekistán", "Vanuatu", "Vaticano", "Venezuela",
        "Vietnam", "Yemen", "Yibuti", "Zambia", "Zimbabue"
    ];


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
    document.getElementById('anio_hasta').addEventListener('change', function() {
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
    
    // Agregar miembro actual
    document.getElementById('addCurrentMember').addEventListener('click', function() {
        currentMemberCount++;
        const html = `
            <div class="member-group" id="currentMember${currentMemberCount}">
                <h5>Miembro ${currentMemberCount}</h5>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="currentMemberName${currentMemberCount}" class="form-label">Nombre*</label>
                        <input type="text" class="form-control" id="currentMemberName${currentMemberCount}" 
                               name="currentMemberName${currentMemberCount}" required>
                    </div>
                    <div class="col-md-4">
                        <label for="currentMemberInstrument${currentMemberCount}" class="form-label">Instrumento*</label>
                        <input type="text" class="form-control" id="currentMemberInstrument${currentMemberCount}" 
                               name="currentMemberInstrument${currentMemberCount}" required>
                    </div>
                    <div class="col-md-4">
                        <label for="currentMemberSince${currentMemberCount}" class="form-label">Activo desde*</label>
                        <select class="form-select" id="currentMemberSince${currentMemberCount}" 
                                name="currentMemberSince${currentMemberCount}" required>
                                <option value="" selected disabled>Seleccione un año</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('currentMembersContainer').insertAdjacentHTML('beforeend', html);
        // Llenar el select de años
        const select = document.getElementById(`currentMemberSince${currentMemberCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select.appendChild(option);
        }
    });
    
    // Quitar último miembro actual
    document.getElementById('removeCurrentMember').addEventListener('click', function() {
        if (currentMemberCount > 0) {
            document.getElementById(`currentMember${currentMemberCount}`).remove();
            currentMemberCount--;
        }
    });





    
    // Agregar miembro antiguo
    document.getElementById('addFormerMember').addEventListener('click', function() {
        formerMemberCount++;
        const html = `
            <div class="member-group" id="formerMember${formerMemberCount}">
                <h5>Miembro Antiguo ${formerMemberCount}</h5>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="formerMemberName${formerMemberCount}" class="form-label">Nombre*</label>
                        <input type="text" class="form-control" id="formerMemberName${formerMemberCount}" 
                               name="formerMemberName${formerMemberCount}" required>
                    </div>
                    <div class="col-md-4">
                        <label for="formerMemberInstrument${formerMemberCount}" class="form-label">Instrumento*</label>
                        <input type="text" class="form-control" id="formerMemberInstrument${formerMemberCount}" 
                               name="formerMemberInstrument${formerMemberCount}" required>
                    </div>
                    <div class="col-md-2">
                        <label for="formerMemberSince${formerMemberCount}" class="form-label">Desde*</label>
                        <select class="form-select" id="formerMemberSince${formerMemberCount}" 
                                name="formerMemberSince${formerMemberCount}" required>
                            <option value="" selected disabled>Seleccione un año</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                    <div class="col-md-2">
                        <label for="formerMemberUntil${formerMemberCount}" class="form-label">Hasta*</label>
                        <select class="form-select" id="formerMemberUntil${formerMemberCount}" 
                                name="formerMemberUntil${formerMemberCount}" required>
                            <option value="" selected disabled>Seleccione un año</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                </div>
            </div>
        `;
        document.getElementById('formerMembersContainer').insertAdjacentHTML('beforeend', html);
                // Llenar el select de años
        const select_former_since = document.getElementById(`formerMemberSince${formerMemberCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select_former_since.appendChild(option);
        }

                // Llenar el select de años
        const select_former_until = document.getElementById(`formerMemberUntil${formerMemberCount}`);
        for (let year = 1850; year <= 2025; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            select_former_until.appendChild(option);
        }
    });
    
    // Quitar último miembro antiguo
    document.getElementById('removeFormerMember').addEventListener('click', function() {
        if (formerMemberCount > 0) {
            document.getElementById(`formerMember${formerMemberCount}`).remove();
            formerMemberCount--;
        }
    });
    
    // Agregar álbum
    document.getElementById('addAlbum').addEventListener('click', function() {
        albumCount++;
        const html = `
            <div class="album-group mb-3" id="album${albumCount}">
                <h5>Álbum ${albumCount}</h5>
                <div class="row">
                    <div class="col-md-4 mb-3">
                        <label for="albumName${albumCount}" class="form-label">Nombre del Álbum*</label>
                        <input type="text" class="form-control" id="albumName${albumCount}" 
                               name="albumName${albumCount}" required>
                    </div>
                    <div class="col-md-2 mb-3">
                        <label for="albumYear${albumCount}" class="form-label">Año*</label>
                        <select class="form-select" id="albumYear${albumCount}" 
                                name="albumYear${albumCount}" required>
                            <option value="" selected disabled>Seleccione un año</option>
                            <!-- Opciones serán llenadas por JS -->
                        </select>
                    </div>
                    <div class="col-md-3 mb-3">
                        <label for="albumImage${albumCount}" class="form-label">Imagen</label>
                        <input type="file" class="form-control" id="albumImage${albumCount}" 
                               name="albumImage${albumCount}" accept="image/jpeg">
                        <div class="form-text">JPEG, 1:1, max 5MB</div>
                    </div>
                    <div class="col-md-3 mb-3">
                        <label for="albumDuration${albumCount}" class="form-label">Duración (min)*</label>
                        <input type="number" class="form-control" id="albumDuration${albumCount}" 
                               name="albumDuration${albumCount}" min="1" step="1" required>
                    </div>
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
    });
    
    // Quitar último álbum
    document.getElementById('removeAlbum').addEventListener('click', function() {
        if (albumCount > 0) {
            document.getElementById(`album${albumCount}`).remove();
            albumCount--;
        }
    });
    
    // Validación del formulario antes de enviar
    document.getElementById('artistForm').addEventListener('submit', function(e) {
        e.preventDefault();
        console.log("Formulario de artista enviado");
        // Aquí iría la lógica para enviar los datos al API cuando esté listo
    });
    
    // Inicializar con un miembro actual
    document.getElementById('addCurrentMember').click();
});