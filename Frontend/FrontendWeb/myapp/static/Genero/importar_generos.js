document.getElementById('jsonFileInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.json') && file.type !== 'application/json') {
        alert('Por favor, selecciona un archivo JSON válido.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            const jsonData = JSON.parse(e.target.result);

            const previewContainer = document.getElementById('jsonPreview');
            previewContainer.style.display = 'block';
            document.getElementById('jsonContent').textContent = JSON.stringify(jsonData, null, 2);

            // Almacenar los datos en una variable global para usarlos luego
            window.jsonDataToSend = jsonData;
        } catch (error) {
            console.error('Error al parsear JSON:', error);
            alert('El archivo no contiene JSON válido.');
        }
    };
    reader.readAsText(file);
});

document.getElementById('guardarGeneros').addEventListener('click', function () {
    if (!window.jsonDataToSend) {
        alert('No hay datos JSON para enviar. Por favor, selecciona un archivo primero.');
        return;
    }

    // Crear el contenedor dinámicamente si no existe
    let resultContainer = document.getElementById('resultContainer');
    if (!resultContainer) {
        resultContainer = document.createElement('div');
        resultContainer.id = 'resultContainer';
        resultContainer.className = 'mt-3';
        this.parentNode.insertAdjacentElement('afterend', resultContainer);
    }

    // Enviar los datos al servidor Django
    fetch('/importar_generos/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), // Necesario para Django CSRF
        },
        body: JSON.stringify(window.jsonDataToSend),
    })
    //.then(response => response.json())
        .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                // Si hay errores en la respuesta, lanzar un error con los detalles
                if (data.errores) {
                    throw new Error(data.errores.join('\n'));
                }
                throw new Error(data.error || 'Error desconocido');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            resultContainer.innerHTML = `
                <div class="alert alert-success">
                    Géneros importados exitosamente!
                </div>
            `;
            // Recargar la página después de un tiempo
            setTimeout(() => location.reload(), 2000);
        } else {
            resultContainer.innerHTML = `
                <div class="alert alert-danger">
                    Error: ${data.error || 'Error desconocido'}
                </div>
            `;
        }
    })
    .catch(error => {
        resultContainer.innerHTML = `
            <div class="alert alert-danger">
                ${error.message.split('\n').map(err => `<p>${err}</p>`).join('')}
            </div>
        `;
    });
    resultContainer.style.display = 'block';
});

// Función auxiliar para obtener el token CSRF
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