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
                    card.setAttribute("data-id", exercicio.id);

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
                                        ${exercicio.nome}
                                        <input type="checkbox" class="checkbox-exercicio" value="${exercicio.id}">
                                    </label>
                                    <label class="grupo-muscular">
                                        ${exercicio.grupo_muscular}
                                    </label>
                                </div>
                            </div>
                            <div class="inputs">
                                <div class="inputs-detalhes">
                                    <div>
                                        <h2>Séries:</h2>
                                        <input type="number" placeholder="Ex: 3">
                                    </div>
                                    <div>
                                        <h2>Repetições:</h2>
                                        <input type="number" placeholder="Ex: 12">
                                    </div>
                                    <div>
                                        <h2>Carga:</h2>
                                        <input type="text" placeholder="Kg">
                                    </div>
                                </div>
                                <div class="inputs-observacoes">
                                    <div>
                                        <h2>Observações:</h2>
                                        <input type="text" placeholder="Insira observações se necessários sobre o exercício">
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;

                    const checkbox = card.querySelector(".checkbox-exercicio");

                    checkbox.addEventListener("change", function () {
                        const nome = card.getAttribute("data-nome");
                        const id = card.getAttribute("data-id");

                        if (this.checked) {
                            const clone = card.cloneNode(true);
                            clone.classList.add("clonado");
                            clone.setAttribute("data-id", id);
                            clone.querySelector(".checkbox-exercicio").remove();
                            // Adiciona botão de excluir
                            const botaoExcluir = document.createElement("button");
                            botaoExcluir.className = "botao-excluir";
                            botaoExcluir.innerHTML = `
                                <img src="/static/icones-site/icone-lixo.png" alt="Excluir" style="width: 1em; vertical-align: middle; margin-right: 0.4em;">
                                Excluir do treino
                            `;
                            // Evento de exclusão
                            botaoExcluir.addEventListener("click", () => {
                                clone.remove();
                                // desmarca o checkbox original
                                checkbox.checked = false;
                                atualizarContador();
                            });

                            clone.appendChild(botaoExcluir);
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

    // ADICIONA INPUTS OCULTOS CORRETAMENTE AO ENVIAR O FORMULÁRIO
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        const selecionados = areaSelecionados.querySelectorAll(".clonado");

        selecionados.forEach(card => {
            const id = card.getAttribute("data-id");

            const series = card.querySelector('input[placeholder="Ex: 3"]').value || 0;
            const repeticoes = card.querySelector('input[placeholder="Ex: 12"]').value || 0;
            const carga = card.querySelector('input[placeholder="Kg"]').value || "0";
            const observacoes = card.querySelector('input[placeholder="Insira observações se necessários sobre o exercício"]').value || "";

            const createHidden = (name, value) => {
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = name;
                input.value = value;
                return input;
            };

            form.appendChild(createHidden("exercicios", id));
            form.appendChild(createHidden("series", series));
            form.appendChild(createHidden("repeticoes", repeticoes));
            form.appendChild(createHidden("carga", carga));
            form.appendChild(createHidden("observacoes", observacoes));
        });
    });
});
