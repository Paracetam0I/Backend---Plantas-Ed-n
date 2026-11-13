from django.apps import AppConfig


# Configuración de la app "contact". Django la carga porque 'contact' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class ContactConfig(AppConfig):
    name = 'contact'
