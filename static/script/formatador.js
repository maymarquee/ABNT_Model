document.addEventListener("DOMContentLoaded", function () {
    // Captura todos os links da barra lateral
    const menuLinks = document.querySelectorAll(".sidebar ul li a");

    // Captura todos os grupos de formulário
    const formGroups = document.querySelectorAll(".form-group");

    // Função para exibir o campo correspondente
    function showField(target) {
        // Esconde todos os campos
        formGroups.forEach(group => group.style.display = "none");

        // Exibe apenas o campo correspondente ao clique
        const fieldToShow = document.getElementById(target);
        if (fieldToShow) {
            fieldToShow.style.display = "block";
        }
    }

    // Adiciona evento de clique para cada link do menu
    menuLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetField = this.getAttribute("data-target");
            showField(targetField);
        });
    });

    // Exibe o primeiro campo por padrão
    showField("nome_do_arquivo");
});

// script.js
function applyStyle(command) {
    const textarea = document.getElementById('editor');
    const selectedText = textarea.value.substring(textarea.selectionStart, textarea.selectionEnd);

    let formattedText;

    switch(command) {
        case 'bold':
            formattedText = `**${selectedText}**`;
            break;
        case 'italic':
            formattedText = `*${selectedText}*`;
            break;
        case 'underline':
            formattedText = `__${selectedText}__`;
            break;
        case 'insertOrderedList':
            formattedText = `1. ${selectedText.split('\n').join('\n1. ')}`;
            break;
        case 'insertUnorderedList':
            formattedText = `• ${selectedText.split('\n').join('\n• ')}`;
            break;
        default:
            formattedText = selectedText;
    }

    textarea.setRangeText(formattedText, textarea.selectionStart, textarea.selectionEnd, 'select');
    textarea.focus();
}
