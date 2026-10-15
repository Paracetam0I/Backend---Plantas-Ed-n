from django.test import TestCase
from django.urls import reverse


class CoreViewTests(TestCase):

    def test_pagina_responde_200_con_su_template(self):
        # Portada: la página carga y hereda de la plantilla base
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertTemplateUsed(response, "core/base.html")
        self.assertContains(response, "Nuestras plantas")

    def test_admin_redirige_al_login(self):
        # El Panel de Django exige iniciar sesión
        response = self.client.get("/admin/")
        self.assertRedirects(response, "/admin/login/?next=/admin/")
