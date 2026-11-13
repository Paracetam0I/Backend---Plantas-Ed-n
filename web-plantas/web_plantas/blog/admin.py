from django.contrib import admin
from .models import Post


# Clase para configurar cómo se ven y administran las publicaciones en el Panel de Django
class PostAdmin(admin.ModelAdmin):
    # created/updated son automáticos (auto_now_add / auto_now): se muestran solo como lectura.
    # Sin esta línea no aparecerían en el formulario de edición.
    readonly_fields = ('created', 'updated')
    # Columnas que se ven en el listado de publicaciones (sin esto solo se ve el __str__)
    list_display = ('title', 'author', 'category', 'created', 'updated')
    # Panel lateral de filtros por categoría y por fecha
    list_filter = ('category', 'created')
    # Agrega una barra de búsqueda que busca en estos campos
    search_fields = ('title', 'content', 'author')


# Registra el modelo en el admin usando la configuración de PostAdmin.
# Sin esta línea, "Publicaciones" no aparece en el panel y no se pueden cargar datos desde ahí.
admin.site.register(Post, PostAdmin)

# Títulos personalizados del Panel de Django
admin.site.site_header = "Plantas Edén - Administración"  # Encabezado azul de cada página del admin
admin.site.site_title = "Plantas Edén"                    # Texto de la pestaña del navegador
