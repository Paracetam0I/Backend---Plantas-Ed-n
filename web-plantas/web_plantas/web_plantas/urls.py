# Rutas generales del sitio Plantas Edén
# Django recorre urlpatterns de arriba hacia abajo y ejecuta la vista de la primera ruta que coincida.
# Si ninguna coincide, responde 404.
from django.contrib import admin
from django.urls import path
# Se importan las vistas de cada app con un alias, porque todos los módulos se llaman "views"
from core import views as views_core
from about import views as views_about
from contact import views as views_contact
from blog import views as views_blog
from gallery import views as views_gallery
from django.conf import settings

urlpatterns = [
    # path(ruta, vista, name=...). El "name" se usa en las plantillas con {% url 'home' %},
    # así si cambia la ruta (ej. 'blog/' -> 'noticias/') los enlaces siguen funcionando.
    # Si se borra una línea, esa página da 404 y todo {% url %} que la nombre lanza NoReverseMatch.
    path('', views_core.home, name="home"),                      # Portada: http://127.0.0.1:8000/
    path('admin/', admin.site.urls),                             # Panel de Django (incluye sus propias sub-rutas)
    path('about/', views_about.about, name="about"),             # Nosotros
    path('contact/', views_contact.contact, name="contact"),     # Contacto
    path('blog/', views_blog.blog, name="blog"),                 # Blog dinámico (lee de la BD y pagina)
    # <category_id> captura el trozo de la URL y lo pasa a la vista como argumento: /category/2/ -> category_id="2".
    # En la plantilla se arma con {% url 'category' c.id %}.
    path('category/<category_id>/', views_blog.category, name="category"),  # Posts de una categoría
    path('gallery/', views_gallery.gallery, name="gallery"),     # Tienda (se mantuvo la URL /gallery/)
]

# En modo debug Django sirve los archivos de MEDIA (imágenes subidas desde el admin)
# static() agrega una ruta /media/<archivo> que lee desde MEDIA_ROOT.
# Sin este bloque las publicaciones se guardan igual, pero sus imágenes dan 404 (se ven rotas).
# Con DEBUG = False no se agrega: en producción las sirve el servidor web (Nginx, Apache).
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
