from django.test import TestCase
from django.urls import reverse


class ContactViewTests(TestCase):

    def test_pagina_responde_200_con_su_template(self):
        # Contacto: la página carga y hereda de la plantilla base
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact.html")
        self.assertTemplateUsed(response, "core/base.html")
        self.assertContains(response, "Estamos aquí para ayudarte")
