from django.shortcuts import render

# Create your views here.
# Vista de la página Nosotros, conectada en web_plantas/urls.py con path('about/', ...) name="about".
# No consulta la BD: render() solo devuelve la plantilla sin contexto (no se le pasa diccionario).
# Django busca la ruta "about/about.html" dentro de about/templates/ gracias a APP_DIRS = True.
def about(request):
    return render(request, "about/about.html")
