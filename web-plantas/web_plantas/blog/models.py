from django.db import models


class Post(models.Model):
    # Opciones de categoría para clasificar las publicaciones del blog
    CATEGORIAS = [
        ('interior', 'Plantas de interior'),
        ('exterior', 'Plantas de exterior'),
        ('semillas', 'Semillas de temporada'),
        ('cuidados', 'Cuidados y consejos'),
    ]

    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(max_length=200, verbose_name="Subtítulo")
    content = models.TextField(verbose_name="Contenido")
    author = models.CharField(max_length=100, verbose_name="Autor")
    category = models.CharField(max_length=20, choices=CATEGORIAS, default='interior', verbose_name="Categoría")
    image = models.ImageField(upload_to="blog", verbose_name="Imagen")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        # Orden por defecto: más recientes primero (evita el aviso de lista sin orden del Paginator)
        ordering = ['-created']

    def __str__(self):
        return self.title
