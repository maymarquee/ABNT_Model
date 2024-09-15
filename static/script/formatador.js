document.addEventListener("DOMContentLoaded", function () {

    const menuLinks = document.querySelectorAll(".sidebar ul li a");


    const formGroups = document.querySelectorAll(".form-group");


    function showField(target) {

        formGroups.forEach(group => group.style.display = "none");


        const fieldToShow = document.getElementById(target);
        if (fieldToShow) {
            fieldToShow.style.display = "block";
        }
    }


    menuLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const targetField = this.getAttribute("data-target");
            showField(targetField);
        });
    });


    showField("nome_do_arquivo");
});

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

