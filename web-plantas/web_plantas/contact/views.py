from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
# Vista de la página Contacto, conectada en web_plantas/urls.py con path('contact/', ...) name="contact".
# Crea el formulario vacío y lo pasa a la plantilla como 'form'.
# Todavía no procesa el envío (POST): al enviar, la página se vuelve a mostrar con el formulario vacío.
# Django busca la ruta "contact/contact.html" dentro de contact/templates/ gracias a APP_DIRS = True.
def contact(request):
    contact_form = ContactForm()
    return render(request, "contact/contact.html", {'form': contact_form})
