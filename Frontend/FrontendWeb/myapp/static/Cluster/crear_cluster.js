document.addEventListener('DOMContentLoaded', function () {
    const descripcionInput = document.getElementById('descripcion');
    const charCount = document.getElementById('charCount');

    // Contador de caracteres para la descripción
    descripcionInput.addEventListener('input', function () {
        const remaining = 300 - this.value.length;
        charCount.textContent = remaining;
        charCount.style.color = remaining < 0 ? '#dc3545' : '#6c757d';
    });

    // Validación básica del formulario
    document.getElementById('clusterForm').addEventListener('submit', function (e) {
        let isValid = true;
        const nombre = document.getElementById('nombre').value.trim();
        const descripcion = descripcionInput.value.trim();
        // Validar nombre
        if (nombre.length < 3 || nombre.length > 30) {
            document.getElementById('nombreError').style.display = 'block';
            isValid = false;
        }

        // Validar descripción
        if (descripcion.length > 300) {
            document.getElementById('descripcionError').style.display = 'block';
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault(); // Detener envío si hay errores
        }
    });
});