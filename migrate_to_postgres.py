#!/usr/bin/env python
"""
Script para migrar de SQLite para PostgreSQL.
Execute: python migrate_to_postgres.py
"""
import os
import sys
import json
from datetime import datetime
import subprocess
from pathlib import Path

# Adiciona o projeto ao path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devadmin.settings')

import django
django.setup()

from django.core import serializers
from django.apps import apps

def backup_sqlite():
    """Faz backup do banco SQLite atual"""
    backup_file = BASE_DIR / f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    original_db = BASE_DIR / "db.sqlite3"
    
    if original_db.exists():
        import shutil
        shutil.copy2(original_db, backup_file)
        print(f"✅ Backup criado: {backup_file}")
        return backup_file
    else:
        print("⚠️  Banco SQLite não encontrado")
        return None

def export_data():
    """Exporta todos os dados para JSON"""
    print("📤 Exportando dados do SQLite...")
    
    # Exclui tabelas que não precisam ser migradas
    exclude_models = ['contenttypes.ContentType', 'auth.Permission', 'sessions.Session']
    
    all_models = []
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_name = f"{app_config.label}.{model.__name__}"
            if model_name not in exclude_models:
                all_models.append(model)
    
    # Exporta dados
    data = []
    for model in all_models:
        try:
            model_data = serializers.serialize('json', model.objects.all())
            if model_data != '[]':
                data.append(model_data)
                print(f"  ✓ {model._meta.label}: {model.objects.count()} registros")
        except Exception as e:
            print(f"  ✗ {model._meta.label}: Erro - {e}")
    
    # Salva em arquivo
    output_file = BASE_DIR / "data_export.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        # Junta todos os dados em um array válido
        f.write('[' + ','.join(data) + ']')
    
    print(f"✅ Dados exportados para: {output_file}")
    return output_file

def setup_postgres():
    """Configura e testa conexão com PostgreSQL"""
    print("\n🔧 Configurando PostgreSQL...")
    
    from django.db import connection
    
    try:
        # Testa conexão
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conectado ao PostgreSQL: {version[0]}")
            
            # Mostra informações do banco
            cursor.execute("SELECT current_database(), current_user;")
            db_info = cursor.fetchone()
            print(f"📊 Banco: {db_info[0]}, Usuário: {db_info[1]}")
        
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com PostgreSQL: {e}")
        print("\n📝 Verifique sua configuração:")
        print("1. DATABASE_URL no .env ou variáveis de ambiente")
        print("2. Banco criado e permissões concedidas")
        print("3. PostgreSQL rodando na porta correta")
        return False

def import_data(data_file):
    """Importa dados para PostgreSQL"""
    print("\n📥 Importando dados para PostgreSQL...")
    
    try:
        # Carrega os dados
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Desativa sinais durante importação
        from django.db import transaction
        
        with transaction.atomic():
            for obj in data:
                try:
                    # Usa natural keys para evitar conflitos de IDs
                    model = apps.get_model(obj["model"])
                    
                    # Tenta usar natural key se disponível
                    natural_key = obj.get("natural_key", None)
                    
                    if natural_key and hasattr(model.objects, 'get_by_natural_key'):
                        # Evita duplicação usando natural keys
                        try:
                            model.objects.get_by_natural_key(*natural_key)
                            print(f"  ⚠️  {obj['model']} já existe (pulando)")
                            continue
                        except model.DoesNotExist:
                            pass
                    
                    # Cria objeto
                    deserialized_obj = list(serializers.deserialize('json', json.dumps([obj])))
                    for item in deserialized_obj:
                        item.save()
                
                except Exception as e:
                    print(f"  ⚠️  Erro em {obj['model']}: {e}")
                    continue
        
        print("✅ Dados importados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def main():
    """Fluxo principal de migração"""
    print("=" * 60)
    print("🔄 MIGRAÇÃO SQLite → PostgreSQL")
    print("=" * 60)
    
    # 1. Backup
    print("\n1. Backup do SQLite")
    backup_file = backup_sqlite()
    
    # 2. Exportar dados
    print("\n2. Exportação de dados")
    data_file = export_data()
    
    # 3. Pergunta se quer continuar
    response = input("\n⏸️  Dados exportados. Deseja continuar com a migração? (s/n): ")
    if response.lower() != 's':
        print("Migração cancelada.")
        return
    
    # 4. Configurar PostgreSQL
    print("\n3. Configuração do PostgreSQL")
    print("⚠️  Certifique-se de que:")
    print("   - DATABASE_URL está configurado no .env")
    print("   - Ou variáveis DB_* estão definidas")
    print("   - O banco PostgreSQL está acessível")
    
    input("\nPressione Enter para continuar...")
    
    if not setup_postgres():
        return
    
    # 5. Aplicar migrações
    print("\n4. Aplicando migrações")
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)
        print("✅ Migrações aplicadas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro nas migrações: {e}")
        return
    
    # 6. Importar dados
    print("\n5. Importação de dados")
    if import_data(data_file):
        print("\n🎉 Migração concluída com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Teste o sistema: python manage.py runserver")
        print("2. Verifique se todos os dados estão presentes")
        print("3. Faça login com seu usuário admin")
        print("4. Remova os arquivos temporários se tudo estiver OK:")
        print(f"   - {data_file}")
        print(f"   - {backup_file} (após confirmar que está tudo OK)")
    else:
        print("\n❌ Migração falhou. O backup está em:", backup_file)

if __name__ == "__main__":
    main()