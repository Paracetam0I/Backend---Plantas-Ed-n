from django.shortcuts import render

# Create your views here.
# Vista de la página Tienda, conectada en web_plantas/urls.py con path('gallery/', ...) name="gallery".
# No consulta la BD: render() solo devuelve la plantilla sin contexto (no se le pasa diccionario).
# Django busca la ruta "gallery/gallery.html" dentro de gallery/templates/ gracias a APP_DIRS = True.
def gallery(request):
    return render(request, "gallery/gallery.html")
