document.getElementById('jsonFileInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) return;

    // Verificar que el archivo sea JSON
    if (!file.name.endsWith('.json') && file.type !== 'application/json') {
        alert('Por favor, selecciona un archivo JSON válido.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const jsonData = JSON.parse(e.target.result);

            // Mostrar el contenedor
            const previewContainer = document.getElementById('jsonPreview');
            previewContainer.style.display = 'block';

            // Mostrar el contenido formateado
            document.getElementById('jsonContent').textContent =
                JSON.stringify(jsonData, null, 2);

            // También puedes almacenar los datos para enviarlos luego
            // por ejemplo en un campo hidden o en memoria
            // document.getElementById('jsonData').value = e.target.result;

        } catch (error) {
            console.error('Error al parsear JSON:', error);
            alert('El archivo no contiene JSON válido.');
        }
    };
    reader.readAsText(file);

    document.getElementById('guardarGeneros').addEventListener('click', function () {
        console.log("Formulario Enviado");

        // Crear el contenedor dinámicamente si no existe
        let resultContainer = document.getElementById('resultContainer');
        if (!resultContainer) {
            resultContainer = document.createElement('div');
            resultContainer.id = 'resultContainer';
            resultContainer.className = 'mt-3';
            this.parentNode.insertAdjacentElement('afterend', resultContainer);
        }

        resultContainer.innerHTML = '<div class="alert alert-info">Simulación: Formulario listo para enviar</div>';
        resultContainer.style.display = 'block';
    });
});