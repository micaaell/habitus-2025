#!/usr/bin/env bash
# build.sh

set -o errexit  # Sai se algum comando falhar

echo "🔧 Iniciando build..."

# Mostra versão do Python (ajuda no debug)
python --version

# Atualiza pip
pip install --upgrade pip

# Instala dependências
pip install -r requirements.txt

# Aplica migrações do banco de dados
python manage.py migrate --noinput

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

echo "✅ Build concluído com sucesso!"
