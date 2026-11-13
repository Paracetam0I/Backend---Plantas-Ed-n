from django.apps import AppConfig


# Configuración de la app "info". Django la carga porque 'info' está en INSTALLED_APPS.
# name debe coincidir con el nombre de la carpeta; si no, Django no encuentra la app al arrancar.
class InfoConfig(AppConfig):
    name = 'info'
    # Nombre de la sección en el Panel de Django (si no, mostraría "Info")
    verbose_name = 'Información del negocio'
