"""
WSGI config for web_plantas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""
# WSGI: interfaz estándar (síncrona) entre un servidor web de producción (Gunicorn, Apache mod_wsgi)
# y Django. runserver no lo necesita directamente, pero lo usa como referencia (WSGI_APPLICATION).

import os

from django.core.wsgi import get_wsgi_application

# Igual que en manage.py: indica qué settings cargar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_plantas.settings')

# Objeto que el servidor web llama en cada petición HTTP
application = get_wsgi_application()
