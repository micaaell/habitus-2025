
# Configurações Django automáticas
export DJANGO_SETTINGS_MODULE=devadmin.settings
export PYTHONPATH="$PYTHONPATH:/workspaces/habitus-2025"
alias django-check="DJANGO_SETTINGS_MODULE=devadmin.settings python manage.py check --deploy"
alias django-run="DJANGO_SETTINGS_MODULE=devadmin.settings python manage.py runserver"
