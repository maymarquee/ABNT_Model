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
