import os
import sys
import django

print("🔍 DIAGNÓSTICO COMPLETO")

# 1. Verifica caminhos
print("\n1. Caminhos do Python:")
for path in sys.path:
    print(f"   {path}")

# 2. Verifica variáveis de ambiente
print("\n2. Variáveis de ambiente:")
env_vars = ['DJANGO_SETTINGS_MODULE', 'PYTHONPATH', 'SECRET_KEY', 'DEBUG']
for var in env_vars:
    value = os.environ.get(var, 'NÃO DEFINIDA')
    print(f"   {var}: {value}")

# 3. Tenta importar settings
print("\n3. Tentando importar settings...")
try:
    from django.conf import settings
    
    print(f"   ✅ Settings importado: {settings.SETTINGS_MODULE}")
    print(f"   📁 Caminho do arquivo: {settings.__file__}")
    
    # 4. Verifica configurações críticas
    print("\n4. Configurações críticas:")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   SECRET_KEY (tamanho): {len(getattr(settings, 'SECRET_KEY', ''))}")
    
    # 5. Verifica MIDDLEWARE
    print("\n5. MIDDLEWARE:")
    middleware_list = getattr(settings, 'MIDDLEWARE', [])
    has_csrf = any('csrf' in m.lower() for m in middleware_list)
    print(f"   Total de middlewares: {len(middleware_list)}")
    print(f"   Tem CSRF middleware: {has_csrf}")
    
    if not has_csrf:
        print("   ❌ CSRF middleware NÃO encontrado!")
        print("   Lista completa:")
        for i, m in enumerate(middleware_list, 1):
            print(f"     {i}. {m}")
    
except Exception as e:
    print(f"   ❌ Erro ao importar settings: {e}")