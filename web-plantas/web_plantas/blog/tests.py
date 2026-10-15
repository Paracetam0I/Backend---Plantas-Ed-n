import io
import shutil
import tempfile
from datetime import datetime, timedelta, timezone as dt_timezone
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from django.db import models
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from .models import Post

# Carpeta temporal para las imágenes subidas en las pruebas (no se toca media/ real)
MEDIA_TEMPORAL = tempfile.mkdtemp()


def imagen_de_prueba(nombre="prueba.gif"):
    # Imagen GIF mínima válida generada en memoria con Pillow
    buffer = io.BytesIO()
    Image.new("RGB", (2, 2), (34, 139, 34)).save(buffer, format="GIF")
    return SimpleUploadedFile(nombre, buffer.getvalue(), content_type="image/gif")


def tearDownModule():
    # Al terminar todas las pruebas del módulo se borra la carpeta temporal
    shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)


def crear_post(numero=1, **extra):
    datos = {
        "title": f"Publicación {numero}",
        "subtitle": f"Subtítulo {numero}",
        "content": "Contenido de prueba.",
        "author": "Equipo Plantas Edén",
        "category": "cuidados",
        "image": imagen_de_prueba(f"post{numero}.gif"),
    }
    datos.update(extra)
    return Post.objects.create(**datos)


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class PostModelTests(TestCase):

    def test_campos_obligatorios_del_modelo(self):
        # El profesor exige image, created y updated, y al menos 6 atributos
        self.assertIsInstance(Post._meta.get_field("image"), models.ImageField)
        created = Post._meta.get_field("created")
        updated = Post._meta.get_field("updated")
        self.assertIsInstance(created, models.DateTimeField)
        self.assertIsInstance(updated, models.DateTimeField)
        self.assertTrue(created.auto_now_add)
        self.assertTrue(updated.auto_now)
        campos = [f for f in Post._meta.concrete_fields if f.name != "id"]
        self.assertGreaterEqual(len(campos), 6)

    def test_imagen_se_guarda_en_carpeta_blog(self):
        post = crear_post()
        self.assertTrue(post.image.name.startswith("blog/"))
        self.assertTrue(post.image.url.startswith("/media/blog/"))

    def test_created_no_cambia_y_updated_si(self):
        post = crear_post()
        created_original = post.created
        updated_original = post.updated
        # Se simula que la edición ocurre una hora después
        mas_tarde = timezone.now() + timedelta(hours=1)
        with mock.patch("django.utils.timezone.now", return_value=mas_tarde):
            post.title = "Título editado"
            post.save()
        post.refresh_from_db()
        self.assertEqual(post.created, created_original)
        self.assertGreater(post.updated, updated_original)
        self.assertEqual(post.updated, mas_tarde)

    def test_str_devuelve_el_titulo(self):
        post = crear_post(title="Cuidados de la lavanda")
        self.assertEqual(str(post), "Cuidados de la lavanda")

    def test_orden_por_defecto_mas_reciente_primero(self):
        self.assertEqual(Post._meta.ordering, ["-created"])
        antiguo = crear_post(1)
        nuevo = crear_post(2)
        Post.objects.filter(pk=antiguo.pk).update(created=timezone.now() - timedelta(days=5))
        self.assertEqual(list(Post.objects.all()), [nuevo, antiguo])


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class BlogViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 10 publicaciones con fechas distintas: la nº 10 es la más reciente
        base = datetime(2026, 8, 1, 15, 0, tzinfo=dt_timezone.utc)
        for i in range(1, 11):
            post = crear_post(i)
            Post.objects.filter(pk=post.pk).update(created=base + timedelta(days=i))

    def titulos(self, response):
        return [p.title for p in response.context["posts"]]

    def test_blog_responde_200_con_su_template(self):
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/blog.html")
        self.assertTemplateUsed(response, "core/base.html")

    def test_contexto_posts_es_una_pagina(self):
        response = self.client.get(reverse("blog"))
        self.assertIn("posts", response.context)
        self.assertIsInstance(response.context["posts"], Page)

    def test_paginacion_de_3_por_pagina(self):
        response = self.client.get(reverse("blog"))
        posts = response.context["posts"]
        self.assertEqual(posts.paginator.per_page, 3)
        self.assertEqual(posts.paginator.count, 10)
        self.assertEqual(posts.paginator.num_pages, 4)
        for pagina, cantidad in [(1, 3), (2, 3), (3, 3), (4, 1)]:
            response = self.client.get(reverse("blog"), {"page": pagina})
            self.assertEqual(len(response.context["posts"]), cantidad)
            self.assertContains(response, f"Página {pagina} de 4")

    def test_paginas_sin_duplicados_y_ordenadas(self):
        todos = []
        for pagina in range(1, 5):
            todos += self.titulos(self.client.get(reverse("blog"), {"page": pagina}))
        esperado = [f"Publicación {i}" for i in range(10, 0, -1)]
        self.assertEqual(todos, esperado)

    def test_pagina_invalida_muestra_la_primera(self):
        response = self.client.get(reverse("blog"), {"page": "abc"})
        self.assertEqual(response.context["posts"].number, 1)
        self.assertEqual(self.titulos(response)[0], "Publicación 10")

    def test_pagina_fuera_de_rango_muestra_la_ultima(self):
        response = self.client.get(reverse("blog"), {"page": 99})
        self.assertEqual(response.context["posts"].number, 4)
        self.assertEqual(self.titulos(response), ["Publicación 1"])

    def test_enlaces_de_paginacion(self):
        primera = self.client.get(reverse("blog"))
        self.assertNotContains(primera, "Anterior")
        self.assertContains(primera, "?page=2")
        self.assertContains(primera, "?page=4")
        ultima = self.client.get(reverse("blog"), {"page": 4})
        self.assertNotContains(ultima, "Siguiente")
        self.assertContains(ultima, "?page=3")

    def test_muestra_campos_del_post(self):
        post = Post.objects.get(title="Publicación 10")
        response = self.client.get(reverse("blog"))
        self.assertContains(response, post.subtitle)
        self.assertContains(response, post.author)
        self.assertContains(response, post.get_category_display())
        self.assertContains(response, post.image.url)

    def test_formato_de_fecha_sin_cero_inicial(self):
        # 7 de octubre a mediodía en Chile: debe mostrarse "7 de octubre", no "07 de octubre"
        post = Post.objects.get(title="Publicación 10")
        Post.objects.filter(pk=post.pk).update(created=datetime(2026, 10, 7, 15, 0, tzinfo=dt_timezone.utc))
        response = self.client.get(reverse("blog"))
        self.assertContains(response, "7 de octubre de 2026")
        self.assertNotContains(response, "07 de octubre")

    def test_blog_vacio_muestra_mensaje(self):
        Post.objects.all().delete()
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Muy pronto")
