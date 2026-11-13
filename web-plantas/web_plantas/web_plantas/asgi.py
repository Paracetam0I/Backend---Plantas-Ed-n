"""
ASGI config for web_plantas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""
# ASGI: versión asíncrona de WSGI (Uvicorn, Daphne). Permite websockets y vistas async.
# Este proyecto no lo usa; Django lo genera por defecto con startproject.

import os

from django.core.asgi import get_asgi_application

# Igual que en manage.py: indica qué settings cargar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_plantas.settings')

# Objeto que el servidor ASGI llama en cada conexión
application = get_asgi_application()
