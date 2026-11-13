from django.apps import AppConfig


# Configuración de la app "blog". Django la carga porque 'blog' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class BlogConfig(AppConfig):
    name = 'blog'
