function toggleDarkMode(event) {
    event.preventDefault(); 
    
    const body = document.body;
    body.classList.toggle('dark-mode'); // adiciona ou remove a classe 'dark-mode'

    // se o modo escuro está ativado, salvamos a preferência no localStorage
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}

// carrega a preferência de dark mode ao carregar a página
function loadDarkModePreference() {
    const darkMode = localStorage.getItem('darkMode');

    // se a preferência for "enabled", ativamos o modo escuro
    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
    }
}

// executa ao carregar a página
loadDarkModePreference();

document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);

