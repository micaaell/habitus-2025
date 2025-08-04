function toggleSenha() {
    const senhaInput = document.getElementById("senha");
    const olhoIcone = document.getElementById("iconeSenha")
    if (senhaInput.type === "password") {
        senhaInput.type = "text";
        olhoIcone.src = "{% static 'icones-site/olho_aberto.png' %}";
    } else {
        senhaInput.type = "password";
        olhoIcone.src = "{% static 'icones-site/olho_fechado.png' %}";
    }
}


window.addEventListener('DOMContentLoaded', () => {
            const errorToast = document.getElementById('error-toast');
            if (errorToast) {
                setTimeout(() => {
                    errorToast.style.opacity = '0';
                    setTimeout(() => {
                        errorToast.style.display = 'none';
                    }, 500); // tempo da transição CSS
                }, 5000); // 5 segundos visível
            }
        });