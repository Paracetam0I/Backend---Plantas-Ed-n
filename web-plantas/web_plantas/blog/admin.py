from django.contrib import admin
from .models import Post, Category, Author


# Clase para configurar cómo se ven y administran las publicaciones en el Panel de Django.
# Sobrescribe el ModelAdmin por defecto; tiene 7 atributos de configuración.
class PostAdmin(admin.ModelAdmin):
    # 1. created/updated son automáticos (auto_now_add / auto_now): se muestran solo como lectura.
    # Sin esta línea no aparecerían en el formulario de edición.
    readonly_fields = ('created', 'updated')
    # 2. Columnas que se ven en el listado de publicaciones (sin esto solo se ve el __str__)
    list_display = ('title', 'published', 'author')
    # 3. Orden del listado: primero por autor y dentro de cada autor por fecha de publicación.
    # Ordenar por una ForeignKey usa el Meta.ordering de Author (por nombre).
    ordering = ('author', 'published')
    # 4. Barra de búsqueda. author__name busca dentro del campo name del modelo relacionado Author
    # (el doble guion bajo recorre la relación; buscar solo por 'author' daría error porque es una FK).
    search_fields = ('title', 'author__name')
    # 5. Navegación por año / mes / día sobre la fecha de publicación, arriba del listado
    date_hierarchy = 'published'
    # 6. Panel lateral de filtros por categoría y por autor
    list_filter = ('categories', 'author')
    # 7. Para el ManyToMany: en vez de una lista de selección múltiple (que obliga a usar Ctrl),
    # muestra dos cajas "disponibles / elegidas" con buscador y flechas.
    filter_horizontal = ('categories',)


# Configuración de los modelos relacionados: solo hace falta mostrar las fechas automáticas
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('name', 'specialty')


# Registra cada modelo en el admin con su configuración.
# Sin estas líneas el modelo no aparece en el panel y no se pueden cargar datos desde ahí.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)

# Títulos personalizados del Panel de Django
admin.site.site_header = "Plantas Edén - Administración"  # Encabezado azul de cada página del admin
admin.site.site_title = "Plantas Edén"                    # Texto de la pestaña del navegador
