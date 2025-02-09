document.addEventListener("DOMContentLoaded", function () {
    let modal = document.getElementById("modalConfirm");
    let confirmBtn = document.getElementById("confirmarExclusaoBtn");
    let pacienteId = null;

    // Função para abrir o modal de exclusão
    window.confirmarExclusao = function (id) {
        pacienteId = id;
        modal.style.display = "block";
    };

    // Função para excluir o paciente
    window.excluirPaciente = function () {
        if (pacienteId) {
            fetch(`/pacientes/excluir/${pacienteId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),  // ✅ Garantia do CSRF Token
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Paciente excluído com sucesso!");
                    location.reload();  // ✅ Atualiza a página após excluir
                } else {
                    alert("Erro ao excluir paciente: " + data.error);
                }
            })
            .catch(error => console.error("Erro:", error));
        }
        fecharModal();
    };

    // Função para fechar o modal
    window.fecharModal = function () {
        modal.style.display = "none";
    };

    // Função para obter o CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
