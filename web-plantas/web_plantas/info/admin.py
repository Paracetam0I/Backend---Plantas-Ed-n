from django.contrib import admin
from .models import BusinessInfo


class BusinessInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    # Muestra clave y valor en el listado para editar rápido sin abrir cada registro
    list_display = ('name', 'key', 'value')


# Registra el modelo: aparece en el panel como "Datos del negocio"
admin.site.register(BusinessInfo, BusinessInfoAdmin)
