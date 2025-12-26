import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devadmin.settings')
django.setup()

from django.conf import settings

print("🔍 Verificando configurações de CSRF:")
print(f"DEBUG = {settings.DEBUG}")
print(f"MIDDLEWARE contém CSRF: {'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE}")
print(f"CSRF middleware exato: {[m for m in settings.MIDDLEWARE if 'csrf' in m.lower()]}")
print(f"Tamanho da SECRET_KEY: {len(settings.SECRET_KEY)}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")