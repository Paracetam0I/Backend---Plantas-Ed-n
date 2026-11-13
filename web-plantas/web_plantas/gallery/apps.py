from django.apps import AppConfig


# Configuración de la app "gallery". Django la carga porque 'gallery' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class GalleryConfig(AppConfig):
    name = 'gallery'
