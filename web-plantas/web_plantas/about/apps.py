from django.apps import AppConfig


# Configuración de la app "about". Django la carga porque 'about' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class AboutConfig(AppConfig):
    name = 'about'
