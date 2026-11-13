from django.shortcuts import render


# La app core además contiene base.html (plantilla padre de todo el sitio)
# y los archivos estáticos del template Dopetrope (core/static/core/assets/).

# Create your views here.
# Vista de la página Portada (Home), conectada en web_plantas/urls.py con path('', ...) name="home".
# No consulta la BD: render() solo devuelve la plantilla sin contexto (no se le pasa diccionario).
# Django busca la ruta "core/index.html" dentro de core/templates/ gracias a APP_DIRS = True.
def home(request):
    return render(request, "core/index.html")
