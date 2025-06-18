document.addEventListener('DOMContentLoaded', function() {
    let subgenreCount = 0;
    
    // Cargar géneros principales al iniciar
    cargarGenerosPrincipales();

    // Mostrar/ocultar subgéneros según checkbox
    document.getElementById('includeSubgenres').addEventListener('change', function() {
        document.getElementById('subgenresContainer').style.display = 
            this.checked ? 'block' : 'none';
    });

    // Manejar envío del formulario
    document.getElementById('searchForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const artistName = document.getElementById('artistName').value.trim();
        const mainGenre = document.getElementById('mainGenre').value;
        
        if (!mainGenre) {
            alert('Por favor selecciona un género principal');
            return;
        }
        
        // Obtener subgéneros seleccionados
        const subgenres = [];
        const subgenreSelects = document.querySelectorAll('.subgenre-select');
        subgenreSelects.forEach(select => {
            if (select.value) subgenres.push(select.value);
        });

        try {
            // Mostrar carga
            document.getElementById('resultsContainer').style.display = 'block';
            document.getElementById('artistResults').innerHTML = '<p>Buscando artistas...</p>';
            document.getElementById('noResults').style.display = 'none';
            
            // Realizar búsqueda
            const response = await fetch('/buscar_artista_genero/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    artist_name: artistName,
                    main_genre: mainGenre,
                    subgenres: subgenres
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Error en la búsqueda');
            }
            
            mostrarResultados(result.artists);
            
        } catch (error) {
            console.error('Error en la búsqueda:', error);
            document.getElementById('artistResults').innerHTML = `
                <div class="alert alert-danger">
                    ${error.message}
                </div>
            `;
        }
    });

    // Función para cargar géneros principales
    async function cargarGenerosPrincipales() {
        try {
            const response = await fetch('/api/genres/');
            if (!response.ok) throw new Error('Error al cargar géneros');

            const generos = await response.json();
            const select = document.getElementById('mainGenre');

            generos.forEach(genero => {
                const option = document.createElement('option');
                option.value = genero.id;
                option.textContent = genero.nombre;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar géneros. Recargue la página.');
        }
    }

    // Función para agregar subgénero
    document.getElementById('addSubgenre').addEventListener('click', function() {
        subgenreCount++;
        const html = `
            <div class="subgenero-group" id="subgenre${subgenreCount}">
                <div class="mb-3">
                    <label for="subgenreSelect${subgenreCount}" class="form-label">Subgénero ${subgenreCount}</label>
                    <select class="form-select subgenre-select" id="subgenreSelect${subgenreCount}">
                        <option value="" selected disabled>Seleccione un subgénero...</option>
                    </select>
                </div>
            </div>
        `;
        document.getElementById('subgenresList').insertAdjacentHTML('beforeend', html);
        cargarSubgeneros(`subgenreSelect${subgenreCount}`);
    });

    // Función para quitar subgénero
    document.getElementById('removeSubgenre').addEventListener('click', function() {
        if (subgenreCount > 0) {
            document.getElementById(`subgenre${subgenreCount}`).remove();
            subgenreCount--;
        }
    });

    // Función para cargar subgéneros
    async function cargarSubgeneros(selectId) {
        try {
            const response = await fetch('/api/subgenres/');
            if (!response.ok) throw new Error('Error al cargar subgéneros');

            const subgeneros = await response.json();
            const select = document.getElementById(selectId);

            subgeneros.forEach(subgenero => {
                const option = document.createElement('option');
                option.value = subgenero.id;
                option.textContent = subgenero.nombre;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error:', error);
            alert('Error al cargar subgéneros');
        }
    }

    // Función para mostrar resultados
    function mostrarResultados(artists) {
        const resultsContainer = document.getElementById('artistResults');
        const noResults = document.getElementById('noResults');
        
        if (!artists || artists.length === 0) {
            resultsContainer.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }
        
        noResults.style.display = 'none';
        let html = '';
        
        artists.forEach(artist => {
            html += `
                <div class="artist-card">
                    <div class="row">
                        <div class="col-md-9">
                            <h4>${artist.name}</h4>
                            <p><strong>Álbumes:</strong> ${artist.albums_count || 0}</p>
                            <p><strong>Géneros:</strong> ${artist.genres.join(', ')}</p>
                            ${artist.subgenres ? `<p><strong>Subgéneros:</strong> ${artist.subgenres.join(', ')}</p>` : ''}
                        </div>
                    </div>
                </div>
            `;
        });
        
        resultsContainer.innerHTML = html;
    }
});