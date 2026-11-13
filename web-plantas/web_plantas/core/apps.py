from django.apps import AppConfig


# Configuración de la app "core". Django la carga porque 'core' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class CoreConfig(AppConfig):
    name = 'core'
