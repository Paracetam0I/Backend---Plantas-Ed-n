# Pruebas automáticas: se ejecutan con "python manage.py test".
# Django crea una base de datos temporal vacía para las pruebas (no toca db.sqlite3)
# y self.client simula un navegador que hace peticiones GET a las URLs.
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

from .models import Post, Category, Author

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


# Crea y guarda un Post con datos de ejemplo; **extra permite reemplazar cualquier campo.
# El autor y la categoría son modelos relacionados: se reutilizan si ya existen (get_or_create).
def crear_post(numero=1, categorias=("Cuidados y consejos",), **extra):
    autor, _ = Author.objects.get_or_create(name="Equipo Plantas Edén", defaults={"specialty": "Jardinería"})
    datos = {
        "title": f"Publicación {numero}",
        "subtitle": f"Subtítulo {numero}",
        "content": "Contenido de prueba.",
        "author": autor,
        "image": imagen_de_prueba(f"post{numero}.gif"),
    }
    datos.update(extra)
    post = Post.objects.create(**datos)
    # Un ManyToMany solo se puede llenar después de guardar el post (necesita su id)
    for nombre in categorias:
        post.categories.add(Category.objects.get_or_create(name=nombre)[0])
    return post


# Pruebas del modelo Post (campos, fechas automáticas, __str__ y orden)
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
        # upload_to="blog" -> el archivo queda en MEDIA_ROOT/blog/ y su URL empieza con /media/blog/
        post = crear_post()
        self.assertTrue(post.image.name.startswith("blog/"))
        self.assertTrue(post.image.url.startswith("/media/blog/"))

    def test_created_no_cambia_y_updated_si(self):
        # auto_now_add fija created al crear; auto_now actualiza updated en cada save()
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
        # Meta.ordering = ["-published"]: el publicado más recientemente aparece primero
        self.assertEqual(Post._meta.ordering, ["-published"])
        antiguo = crear_post(1)
        nuevo = crear_post(2)
        Post.objects.filter(pk=antiguo.pk).update(published=timezone.now() - timedelta(days=5))
        self.assertEqual(list(Post.objects.all()), [nuevo, antiguo])

    def test_relaciones_con_autor_y_categorias(self):
        # 3 modelos relacionados: Post -> Author (ForeignKey) y Post <-> Category (ManyToMany)
        self.assertIsInstance(Post._meta.get_field("author"), models.ForeignKey)
        self.assertIsInstance(Post._meta.get_field("categories"), models.ManyToManyField)
        post = crear_post(categorias=("Plantas de interior", "Cuidados y consejos"))
        self.assertEqual(post.categories.count(), 2)
        # Relaciones inversas: desde el autor y desde la categoría se llega al post
        self.assertIn(post, post.author.post_set.all())
        self.assertIn(post, Category.objects.get(name="Plantas de interior").post_set.all())

    def test_published_por_defecto_es_ahora(self):
        antes = timezone.now()
        post = crear_post()
        self.assertGreaterEqual(post.published, antes)


# Pruebas de la vista /blog/ (plantilla, paginación y contenido mostrado)
@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class BlogViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 10 publicaciones con fechas distintas: la nº 10 es la más reciente
        base = datetime(2026, 8, 1, 15, 0, tzinfo=dt_timezone.utc)
        for i in range(1, 11):
            post = crear_post(i)
            Post.objects.filter(pk=post.pk).update(published=base + timedelta(days=i))

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
        # 10 publicaciones / 3 por página = 4 páginas (3, 3, 3 y 1)
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
        # Juntando las 4 páginas deben salir las 10 publicaciones, sin repetir y de la 10 a la 1
        todos = []
        for pagina in range(1, 5):
            todos += self.titulos(self.client.get(reverse("blog"), {"page": pagina}))
        esperado = [f"Publicación {i}" for i in range(10, 0, -1)]
        self.assertEqual(todos, esperado)

    def test_pagina_invalida_muestra_la_primera(self):
        # get_page() convierte un valor no numérico en la página 1 (no da error)
        response = self.client.get(reverse("blog"), {"page": "abc"})
        self.assertEqual(response.context["posts"].number, 1)
        self.assertEqual(self.titulos(response)[0], "Publicación 10")

    def test_pagina_fuera_de_rango_muestra_la_ultima(self):
        # get_page() convierte un número demasiado grande en la última página
        response = self.client.get(reverse("blog"), {"page": 99})
        self.assertEqual(response.context["posts"].number, 4)
        self.assertEqual(self.titulos(response), ["Publicación 1"])

    def test_enlaces_de_paginacion(self):
        # En la primera página no hay "Anterior"; en la última no hay "Siguiente"
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
        self.assertContains(response, post.author.name)
        self.assertContains(response, post.image.url)
        # Cada categoría del post aparece como enlace a su página
        categoria = post.categories.first()
        self.assertContains(response, f'href="{reverse("category", args=[categoria.id])}"')

    def test_fecha_en_formato_corto(self):
        # SHORT_DATE_FORMAT con es-cl: 7 de octubre de 2026 -> 07/10/2026
        post = Post.objects.get(title="Publicación 10")
        Post.objects.filter(pk=post.pk).update(published=datetime(2026, 10, 7, 15, 0, tzinfo=dt_timezone.utc))
        response = self.client.get(reverse("blog"))
        self.assertContains(response, "07/10/2026")

    def test_barra_lateral_lista_categorias_de_la_bd(self):
        # Una categoría creada en la BD aparece sola en la barra lateral con su enlace
        nueva = Category.objects.create(name="Huertos urbanos")
        response = self.client.get(reverse("blog"))
        self.assertContains(response, "Huertos urbanos")
        self.assertContains(response, reverse("category", args=[nueva.id]))

    def test_blog_vacio_muestra_mensaje(self):
        # Sin publicaciones se muestra el bloque {% empty %} de la plantilla
        Post.objects.all().delete()
        response = self.client.get(reverse("blog"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Muy pronto")


# Pruebas de la vista /category/<id>/ (get_object_or_404 y posts de la categoría)
@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class CategoryViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.interior = Category.objects.create(name="Plantas de interior")
        cls.exterior = Category.objects.create(name="Plantas de exterior")
        cls.helecho = crear_post(1, categorias=("Plantas de interior",), title="Helecho")
        cls.romero = crear_post(2, categorias=("Plantas de exterior",), title="Romero")
        # Post con dos categorías: debe aparecer en ambas páginas
        cls.riego = crear_post(3, categorias=("Plantas de interior", "Plantas de exterior"), title="Riego")

    def test_responde_200_con_su_template(self):
        response = self.client.get(reverse("category", args=[self.interior.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/category.html")
        self.assertEqual(response.context["category"], self.interior)

    def test_muestra_solo_posts_de_la_categoria(self):
        response = self.client.get(reverse("category", args=[self.interior.id]))
        self.assertContains(response, "Helecho")
        self.assertContains(response, "Riego")
        self.assertNotContains(response, "Romero")

    def test_categoria_inexistente_da_404(self):
        # get_object_or_404 responde 404 en vez de un error 500
        response = self.client.get(reverse("category", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_categoria_sin_posts_muestra_mensaje(self):
        vacia = Category.objects.create(name="Semillas de temporada")
        response = self.client.get(reverse("category", args=[vacia.id]))
        self.assertContains(response, "Todavía no hay publicaciones")

    def test_menu_marca_blog_como_actual(self):
        response = self.client.get(reverse("category", args=[self.interior.id]))
        self.assertContains(response, f'class="current"><a href="{reverse("blog")}"')
