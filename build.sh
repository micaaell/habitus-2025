#!/usr/bin/env bash
# build.sh

set -o errexit  # Sai se algum comando falhar

echo "🔧 Iniciando build no Render..."

# Atualiza pip (importante para evitar erros)
pip install --upgrade pip

# Instala dependências
pip install -r requirements.txt

# Coleta arquivos estáticos (--clear remove arquivos antigos)
python manage.py collectstatic --noinput --clear

# Aplica migrações do banco de dados
python manage.py migrate --noinput

echo "✅ Build concluído!"