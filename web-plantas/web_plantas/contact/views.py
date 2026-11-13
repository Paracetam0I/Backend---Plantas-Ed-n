from django.shortcuts import render

# Create your views here.
# Vista de la página Contacto, conectada en web_plantas/urls.py con path('contact/', ...) name="contact".
# No consulta la BD: render() solo devuelve la plantilla sin contexto (no se le pasa diccionario).
# Django busca la ruta "contact/contact.html" dentro de contact/templates/ gracias a APP_DIRS = True.
def contact(request):
    return render(request, "contact/contact.html")
