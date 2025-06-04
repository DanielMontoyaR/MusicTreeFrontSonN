console.log("Script de crear genero cargado");
document.addEventListener('DOMContentLoaded', function () {
    // Inicializar color picker
    const pickr = Pickr.create({
        el: '#colorPickerButton',
        theme: 'classic',
        default: '#6c84d5',
        components: {
            preview: true,
            opacity: true,
            hue: true,
            interaction: {
                input: true,
                save: true
            }
        }
    });
    //Actualizar cambio de color
    pickr.on('change', (color) => {
        const hexColor = color.toHEXA().toString();
        document.getElementById('colorPreview').style.backgroundColor = hexColor;
        document.getElementById('color').value = hexColor;
    });

    // Establecer color inicial
    document.getElementById('colorPreview').style.backgroundColor = '#6c84d5';

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

    const paisSelect = document.getElementById('country_of_origin');
    paisesONU.sort().forEach(pais => {
        const option = document.createElement('option');
        option.value = pais;
        option.textContent = pais;
        paisSelect.appendChild(option);
    });


    // Llenar años (1850-2025)
    const yearSelect = document.getElementById('creation_year');
    const currentYear = new Date().getFullYear();
    for (let year = 1850; year <= 2025; year++) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        // Seleccionar el año actual por defecto
        if (year === currentYear) option.selected = true;
        yearSelect.appendChild(option);
    }



    // Mostrar/ocultar secciones condicionales
    document.getElementById('asociarCluster').addEventListener('change', function () {
        document.getElementById('clusterSection').style.display = this.checked ? 'block' : 'none';
    });

    document.getElementById('is_subgenre').addEventListener('change', function () {
        const subgeneroSection = document.getElementById('subgeneroSection');
        const colorInput = document.getElementById('color');
        const colorPickerButton = document.getElementById('colorPickerButton');

        document.getElementById('subgeneroSection').style.display = this.checked ? 'block' : 'none';

        subgeneroSection.style.display = this.checked ? 'block' : 'none';

        // Deshabilitar/limpiar color cuando es subgénero
        if (this.checked) {
            colorInput.value = 'none';
            colorInput.disabled = true;
            colorPickerButton.disabled = true;
            document.getElementById('colorPreview').style.backgroundColor = 'transparent';
        } else {
            colorInput.disabled = false;
            colorPickerButton.disabled = false;
            colorInput.value = '#6c84d5'; // Valor por defecto
            document.getElementById('colorPreview').style.backgroundColor = '#6c84d5';
        }

        if (this.checked) {
            cargarGenerosPrincipales();
        }
    });

    // Contador de caracteres
    document.getElementById('descripcion').addEventListener('input', function () {
        const remaining = 1000 - this.value.length;
        document.getElementById('charCount').textContent = remaining;
        document.getElementById('charCount').style.color = remaining < 0 ? '#dc3545' : '#6c757d';
    });

    // Validación del formulario
    document.getElementById('genreForm').addEventListener('submit', function (e) {
        let isValid = true;

        // Si es subgénero, forzar color a 'none'
        if (document.getElementById('is_subgenre').checked) {
            document.getElementById('color').value = 'none';
        }

        // Validar nombre
        const nombre = document.getElementById('nombre').value.trim();
        if (nombre.length < 3 || nombre.length > 30) {
            document.getElementById('nombreError').style.display = 'block';
            isValid = false;
        }

        // Validar descripción
        if (document.getElementById('descripcion').value.length > 1000) {
            document.getElementById('descripcionError').style.display = 'block';
            isValid = false;
        }

        // Validar país
        if (!document.getElementById('country_of_origin').value) {
            document.getElementById('paisError').style.display = 'block';
            isValid = false;
        }

        // Validar BPM
        const bpmMin = parseInt(document.getElementById('bpm_lower').value);
        const bpmMax = parseInt(document.getElementById('bpm_upper').value);
        if (isNaN(bpmMin) || isNaN(bpmMax) || bpmMin < 0 || bpmMax > 250 || bpmMin >= bpmMax) {
            document.getElementById('bpmError').style.display = 'block';
            isValid = false;
        }

        // Validar cluster si está marcado
        if (document.getElementById('asociarCluster').checked &&
            !document.getElementById('cluster_id').value) {
            document.getElementById('clusterError').style.display = 'block';
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
            // Desplazarse al primer error
            document.querySelector('.is-invalid')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        // Validar Promedio de Canciones (0.1 - 0.99)
        const averageMode = parseFloat(document.getElementById('average_mode').value);
        if (isNaN(averageMode) || averageMode < 0.1 || averageMode > 0.99) {
            e.preventDefault();
            document.getElementById('average_mode').classList.add('is-invalid');
            document.getElementById('promedioCancionesError').textContent =
                'El valor debe estar entre 0.1 y 0.99';
            document.getElementById('promedioCancionesError').style.display = 'block';

            // Desplazarse al error
            document.getElementById('average_mode').scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
        //e.preventDefault();
        // Obtener todos los datos del formulario
        const formData = {
            nombre: document.getElementById('nombre').value,
            descripcion: document.getElementById('descripcion').value,
            is_active: document.getElementById('is_active').value,
            color: document.getElementById('color').value,
            country_of_origin: document.getElementById('country_of_origin').value,
            creation_year: document.getElementById('creation_year').value,
            average_mode: document.getElementById('average_mode').value,
            bpm_lower: document.getElementById('bpm_lower').value,
            bpm_upper: document.getElementById('bpm_upper').value,
            dominant_key: document.getElementById('dominant_key').value,
            typical_volume: document.getElementById('typical_volume').value,
            time_signature: document.getElementById('time_signature').value,
            average_duration: document.getElementById('average_duration').value,
            asociarCluster: document.getElementById('asociarCluster').checked,
            cluster_id: document.getElementById('cluster_id').value,
            is_subgenre: document.getElementById('is_subgenre').checked,
            parent_genre_id: document.getElementById('parent_genre_id').value
        };

        // Imprimir en consola
        console.log("Datos del formulario:", formData);


    });

    // Función para cargar clusters
    async function cargarClusters() {
        try {
            const response = await fetch('/api/clusters/');
            if (!response.ok) throw new Error('Error al cargar clusters');

            const clusters = await response.json();
            const select = document.getElementById('cluster_id');

            // Limpiar y poblar el select
            select.innerHTML = '<option value="" selected disabled>Seleccione un cluster</option>';
            clusters.forEach(cluster => {
                const option = new Option(cluster.nombre, cluster.id);
                select.add(option);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar clusters');
        }
    }

    // Función para cargar géneros desde Django
    async function cargarGenerosPrincipales() {
        try {
            const response = await fetch('/api/genres/');
            if (!response.ok) throw new Error('Error al cargar géneros');

            const generos = await response.json();
            const select = document.getElementById('parent_genre_id');

            // Limpiar y poblar el select
            select.innerHTML = '<option value="" selected disabled>Seleccione un género principal</option>';
            generos.forEach(genero => {
                const option = new Option(genero.nombre, genero.id);
                select.add(option);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar géneros');
        }
    }

    // Event listeners
    document.getElementById('asociarCluster').addEventListener('change', function () {
        const section = document.getElementById('clusterSection');
        section.style.display = this.checked ? 'block' : 'none';
        if (this.checked) cargarClusters();
    });

    document.getElementById('is_subgenre').addEventListener('change', function () {
        const section = document.getElementById('subgeneroSection');
        section.style.display = this.checked ? 'block' : 'none';
        if (this.checked) cargarGenerosPrincipales();
    });
});