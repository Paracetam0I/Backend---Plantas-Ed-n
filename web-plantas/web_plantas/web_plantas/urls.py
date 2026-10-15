"""
URL configuration for web_plantas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views as views_core
from about import views as views_about
from contact import views as views_contact
from blog import views as views_blog
from gallery import views as views_gallery

urlpatterns = [
    path('', views_core.home, name="home"),
    path('admin/', admin.site.urls),
    path('about/', views_about.about, name="about"),
    path('contact/', views_contact.contact, name="contact"),
    path('blog/', views_blog.blog, name="blog"),
    path('gallery/', views_gallery.gallery, name="gallery"),
]
