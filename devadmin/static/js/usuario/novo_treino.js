document.addEventListener("DOMContentLoaded", function () {
    const inputBusca = document.getElementById("busca-exercicio");
    const resultados = document.getElementById("resultados-exercicios");
    const areaSelecionados = document.getElementById("exercicios-selecionados");
    const contador = document.getElementById("quant-exercicios");

    function atualizarContador() {
        const total = areaSelecionados.querySelectorAll(".clonado").length;
        contador.innerHTML = `<p>${total} exercício${total === 1 ? '' : 's'} inserido${total === 1 ? '' : 's'} no treino</p>`;
    }

    inputBusca.addEventListener("input", function () {
        const termo = this.value.trim().toLowerCase();
        resultados.innerHTML = "";

        if (termo.length === 0) return;

        fetch(`/buscar-exercicios/?q=${encodeURIComponent(termo)}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(exercicio => {
                    const card = document.createElement("div");
                    card.className = "card-exercicio";
                    card.setAttribute("data-nome", exercicio.nome.toLowerCase());

                    const midia = exercicio.video_url
                        ? `<video class="video-exercicio" autoplay loop muted playsinline>
                               <source src="${exercicio.video_url}" type="video/mp4">
                               Seu navegador não suporta vídeos.
                           </video>`
                        : `<img src="/static/icones-site/sem-video.png" alt="Sem vídeo" class="imagem-exercicio">`;

                    card.innerHTML = `
                        <div class="info-exercicio">
                            <div class="info-texto">
                                ${midia}
                                <div class="texto">
                                    <label>
                                        <input type="checkbox" class="checkbox-exercicio" value="${exercicio.id}">
                                        ${exercicio.nome}
                                    </label>
                                    <label class="grupo-muscular">
                                        ${exercicio.grupo_muscular}
                                    </label>
                                </div>
                            </div>
                            <div class="inputs">
                                <input type="number" placeholder="Séries">
                                <input type="number" placeholder="Repetições">
                                <input type="text" placeholder="Carga (kg)">
                                <input type="text" placeholder="Observações">
                            </div>
                        </div>
                    `;

                    const checkbox = card.querySelector(".checkbox-exercicio");

                    checkbox.addEventListener("change", function () {
                        const nome = card.getAttribute("data-nome");

                        if (this.checked) {
                            const clone = card.cloneNode(true);
                            clone.classList.add("clonado");
                            clone.querySelector(".checkbox-exercicio").remove();
                            areaSelecionados.appendChild(clone);
                        } else {
                            const clones = areaSelecionados.querySelectorAll(".clonado");
                            clones.forEach(c => {
                                if (c.getAttribute("data-nome") === nome) {
                                    c.remove();
                                }
                            });
                        }

                        atualizarContador();
                    });

                    resultados.appendChild(card);
                });
            })
            .catch(err => {
                resultados.innerHTML = "<p>Erro ao buscar exercícios.</p>";
                console.error(err);
            });
    });
});
