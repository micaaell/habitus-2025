
        function previewNovaFoto() {
            const input = document.getElementById('id_nova_foto');
            const preview = document.getElementById('preview-foto');
            const salvarBtn = document.getElementById('salvar-foto-btn');
            const removerBtn = document.getElementById('remover-foto-btn');

            const file = input.files[0];
            if (file) {
                preview.src = URL.createObjectURL(file);
                salvarBtn.style.display = 'inline-block';
                removerBtn.style.display = 'inline-block';
            }
        }

        function removerNovaFoto() {
            const input = document.getElementById('id_nova_foto');
            const preview = document.getElementById('preview-foto');
            const salvarBtn = document.getElementById('salvar-foto-btn');
            const removerBtn = document.getElementById('remover-foto-btn');

            input.value = '';
            preview.src = "{% if aluno.foto_perfil %}{{ aluno.foto_perfil.url }}{% else %}{% static 'icones-site/sem-foto.png' %}{% endif %}";
            salvarBtn.style.display = 'none';
            removerBtn.style.display = 'none';
        }