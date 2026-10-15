# Rutas generales del sitio Plantas Edén
from django.contrib import admin
from django.urls import path
from core import views as views_core
from about import views as views_about
from contact import views as views_contact
from blog import views as views_blog
from gallery import views as views_gallery
from django.conf import settings

urlpatterns = [
    path('', views_core.home, name="home"),
    path('admin/', admin.site.urls),
    path('about/', views_about.about, name="about"),
    path('contact/', views_contact.contact, name="contact"),
    path('blog/', views_blog.blog, name="blog"),
    path('gallery/', views_gallery.gallery, name="gallery"),
]

# En modo debug Django sirve los archivos de MEDIA (imágenes subidas desde el admin)
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
