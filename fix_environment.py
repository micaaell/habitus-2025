#!/usr/bin/env python
# fix_environment.py

import os
import subprocess
import sys

print("🔧 CONFIGURANDO AMBIENTE DJANGO CORRETAMENTE")
print("=" * 60)

# 1. Configura variáveis de ambiente
print("\n1. Configurando variáveis de ambiente...")
env_vars = {
    'DJANGO_SETTINGS_MODULE': 'devadmin.settings',
    'DEBUG': 'False',
    'PYTHONPATH': os.getcwd(),
}

for key, value in env_vars.items():
    os.environ[key] = value
    print(f"   ✅ {key}={value}")

# 2. Verifica se o settings existe
print("\n2. Verificando estrutura do projeto...")
project_path = os.path.join(os.getcwd(), 'devadmin', 'settings.py')
if os.path.exists(project_path):
    print(f"   ✅ settings.py encontrado em: {project_path}")
else:
    print(f"   ❌ settings.py NÃO encontrado!")
    print(f"   Procurando em: {os.getcwd()}")
    for root, dirs, files in os.walk(os.getcwd()):
        if 'settings.py' in files:
            print(f"   Encontrado em: {os.path.join(root, 'settings.py')}")
            # Ajusta o caminho
            relative_path = os.path.relpath(os.path.join(root, 'settings.py'), os.getcwd())
            module_name = relative_path.replace('/', '.').replace('.py', '')
            os.environ['DJANGO_SETTINGS_MODULE'] = module_name
            print(f"   ✅ DJANGO_SETTINGS_MODULE ajustado para: {module_name}")
            break

# 3. Testa a importação
print("\n3. Testando importação do Django...")
try:
    import django
    django.setup()
    from django.conf import settings
    
    print(f"   ✅ Django importado com sucesso!")
    print(f"   📊 Configurações carregadas:")
    print(f"      - DEBUG: {settings.DEBUG}")
    print(f"      - SECRET_KEY: {'*' * len(settings.SECRET_KEY) if settings.SECRET_KEY else 'NÃO DEFINIDA'}")
    print(f"      - ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    
    # Verifica CSRF middleware
    has_csrf = 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE
    print(f"      - CSRF Middleware: {'✅ PRESENTE' if has_csrf else '❌ AUSENTE'}")
    
except Exception as e:
    print(f"   ❌ Erro: {e}")
    print("\n   Solução alternativa:")
    print("   Execute: python -c \"import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devadmin.settings'); import django; django.setup(); print('✅ Django configurado')\"")

# 4. Executa o check --deploy
print("\n4. Executando verificação de segurança...")
try:
    # Usa subprocess para garantir ambiente limpo
    result = subprocess.run(
        [sys.executable, 'manage.py', 'check', '--deploy'],
        env={**os.environ, 'DEBUG': 'False'},
        capture_output=True,
        text=True
    )
    
    print("   Saída do check --deploy:")
    print("   " + "-" * 50)
    print(result.stdout)
    if result.stderr:
        print("   ERROS:")
        print(result.stderr)
    print("   " + "-" * 50)
    
    if result.returncode == 0:
        print("   🎉 TODOS OS WARNINGS RESOLVIDOS!")
    else:
        print("   ⚠️  Ainda há problemas a resolver")
        
except Exception as e:
    print(f"   ❌ Erro ao executar check: {e}")

# 5. Cria arquivo de configuração automática
print("\n5. Criando configuração automática...")
bashrc_content = """
# Configurações Django automáticas
export DJANGO_SETTINGS_MODULE=devadmin.settings
export PYTHONPATH="$PYTHONPATH:/workspaces/habitus-2025"
alias django-check="DJANGO_SETTINGS_MODULE=devadmin.settings python manage.py check --deploy"
alias django-run="DJANGO_SETTINGS_MODULE=devadmin.settings python manage.py runserver"
"""

with open('.django_env.sh', 'w') as f:
    f.write(bashrc_content)
print("   ✅ Arquivo .django_env.sh criado")
print("   📋 Para usar: source .django_env.sh")

print("\n" + "=" * 60)
print("🎯 COMANDOS PARA EXECUTAR AGORA:")
print("1. source .django_env.sh")
print("2. django-check")
print("3. Ou: DJANGO_SETTINGS_MODULE=devadmin.settings python manage.py check --deploy")