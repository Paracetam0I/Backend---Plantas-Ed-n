#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# manage.py: punto de entrada por consola del proyecto.
# Todos los comandos pasan por aquí: runserver, makemigrations, migrate,
# createsuperuser, test, etc. (ej: python manage.py runserver)
import os
import sys


def main():
    """Run administrative tasks."""
    # Le indica a Django qué archivo de configuración usar (web_plantas/settings.py).
    # Sin esta línea Django no sabría dónde están INSTALLED_APPS, DATABASES, etc.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_plantas.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si falla el import, casi siempre es porque no se activó el venv
        # o Django no está instalado (pip install -r requirements.txt)
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Ejecuta el comando escrito en la terminal (sys.argv = ['manage.py', 'runserver', ...])
    execute_from_command_line(sys.argv)


# Solo se ejecuta main() si el archivo se corre directamente, no si se importa
if __name__ == '__main__':
    main()
