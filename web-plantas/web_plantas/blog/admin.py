from django.contrib import admin
from .models import Post


# Clase para configurar cómo se ven y administran las publicaciones en el Panel de Django
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title', 'author', 'category', 'created', 'updated')
    list_filter = ('category', 'created')
    search_fields = ('title', 'content', 'author')


admin.site.register(Post, PostAdmin)

# Títulos personalizados del Panel de Django
admin.site.site_header = "Plantas Edén - Administración"
admin.site.site_title = "Plantas Edén"
