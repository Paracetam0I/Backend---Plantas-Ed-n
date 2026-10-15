from django.test import TestCase
from django.urls import reverse


class GalleryViewTests(TestCase):

    def test_pagina_responde_200_con_su_template(self):
        # Galería: la página carga y hereda de la plantilla base
        response = self.client.get(reverse("gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "gallery/gallery.html")
        self.assertTemplateUsed(response, "core/base.html")
        self.assertContains(response, "Galería y catálogo")
