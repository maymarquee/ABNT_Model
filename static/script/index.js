function toggleDarkMode(event) {
    event.preventDefault(); 
    
    const body = document.body;
    body.classList.toggle('dark-mode'); 

    
    if (body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
}


function loadDarkModePreference() {
    const darkMode = localStorage.getItem('darkMode');


    if (darkMode === 'enabled') {
        document.body.classList.add('dark-mode');
    }
}


loadDarkModePreference();

document.getElementById('dark-mode-toggle').addEventListener('click', toggleDarkMode);

