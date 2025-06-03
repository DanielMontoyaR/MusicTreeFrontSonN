document.addEventListener('DOMContentLoaded', function () {
    const lightModeBtn = document.getElementById('lightModeBtn');
    const darkModeBtn = document.getElementById('darkModeBtn');
    const body = document.body;

    // Verificar si hay un modo guardado en localStorage
    const savedMode = localStorage.getItem('themeMode');
    if (savedMode === 'dark') {
        enableDarkMode();
    }

    lightModeBtn.addEventListener('click', function () {
        disableDarkMode();
    });

    darkModeBtn.addEventListener('click', function () {
        enableDarkMode();
    });

    function enableDarkMode() {
        body.classList.add('dark-mode');
        darkModeBtn.classList.add('active');
        lightModeBtn.classList.remove('active');
        localStorage.setItem('themeMode', 'dark');
    }

    function disableDarkMode() {
        body.classList.remove('dark-mode');
        lightModeBtn.classList.add('active');
        darkModeBtn.classList.remove('active');
        localStorage.setItem('themeMode', 'light');
    }
});