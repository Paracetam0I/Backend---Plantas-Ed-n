from django.test import TestCase
from django.urls import reverse


class AboutViewTests(TestCase):

    def test_pagina_responde_200_con_su_template(self):
        # Nosotros: la página carga y hereda de la plantilla base
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about/about.html")
        self.assertTemplateUsed(response, "core/base.html")
        self.assertContains(response, "Créditos de imágenes")

    def test_footer_enlaza_a_los_creditos(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("about") + "#creditos")
