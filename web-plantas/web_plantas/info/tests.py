# Pruebas del procesador de contexto: los datos del negocio deben llegar a plantillas de distintas apps
from django.test import TestCase
from django.urls import reverse

from .models import BusinessInfo


class ProcesadorDeContextoTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        BusinessInfo.objects.create(key="INFO_CORREO", name="Correo de contacto", value="hola@plantaseden.cl")
        BusinessInfo.objects.create(key="INFO_TELEFONO", name="Teléfono", value="+56 2 1111 2222")
        BusinessInfo.objects.create(key="INFO_HORARIO_SEMANA", name="Horario", value="8:00 a 20:00")

    def test_variables_en_el_contexto_de_cualquier_pagina(self):
        # La vista home no envía INFO_CORREO; lo agrega el procesador registrado en settings
        response = self.client.get(reverse("home"))
        self.assertEqual(response.context["INFO_CORREO"], "hola@plantaseden.cl")

    def test_footer_muestra_datos_de_la_bd(self):
        response = self.client.get(reverse("about"))
        self.assertContains(response, 'href="mailto:hola@plantaseden.cl"')
        # cut:" " deja el teléfono sin espacios dentro del enlace tel:
        self.assertContains(response, 'href="tel:+56211112222"')

    def test_mismo_dato_en_contacto_y_tienda(self):
        # Un solo registro en el panel cambia el horario en dos apps distintas
        for nombre in ("contact", "gallery"):
            response = self.client.get(reverse(nombre))
            self.assertContains(response, "8:00 a 20:00")

    def test_editar_en_el_panel_cambia_el_sitio(self):
        BusinessInfo.objects.filter(key="INFO_CORREO").update(value="nuevo@plantaseden.cl")
        response = self.client.get(reverse("contact"))
        self.assertContains(response, "nuevo@plantaseden.cl")
        self.assertNotContains(response, "hola@plantaseden.cl")
