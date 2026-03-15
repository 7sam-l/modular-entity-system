"""WSGI config for modular_entity_system project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'modular_entity_system.settings.production',
)
application = get_wsgi_application()
