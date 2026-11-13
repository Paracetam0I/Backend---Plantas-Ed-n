from django.db import models


# Modelo Post: cada clase que hereda de models.Model se convierte en una tabla de la BD (blog_post).
# Cada atributo = una columna. Django agrega solo la columna "id" (clave primaria autoincremental).
# Después de cambiar algo aquí hay que correr: makemigrations (crea el archivo) y migrate (lo aplica a la BD).
class Post(models.Model):
    # Opciones de categoría para clasificar las publicaciones del blog
    # Cada tupla es (valor que se guarda en la BD, texto que se muestra al usuario)
    CATEGORIAS = [
        ('interior', 'Plantas de interior'),
        ('exterior', 'Plantas de exterior'),
        ('semillas', 'Semillas de temporada'),
        ('cuidados', 'Cuidados y consejos'),
    ]

    # CharField: texto corto, max_length es obligatorio (VARCHAR). verbose_name = etiqueta en el admin
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(max_length=200, verbose_name="Subtítulo")
    # TextField: texto largo sin límite de caracteres
    content = models.TextField(verbose_name="Contenido")
    author = models.CharField(max_length=100, verbose_name="Autor")
    # choices: en el admin aparece como lista desplegable y solo acepta esos valores.
    # default: valor si no se elige otro. En la plantilla, get_category_display muestra el texto legible.
    category = models.CharField(max_length=20, choices=CATEGORIAS, default='interior', verbose_name="Categoría")
    # ImageField: guarda en la BD solo la ruta del archivo; la imagen física va a MEDIA_ROOT/blog/.
    # Requiere Pillow instalado (si no, makemigrations da error). Es obligatorio al no tener blank=True.
    image = models.ImageField(upload_to="blog", verbose_name="Imagen")
    # auto_now_add: se llena una sola vez, al crear el registro (no se puede editar en el admin)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    # auto_now: se actualiza con la fecha actual cada vez que se guarda (save) el registro
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    # Meta: opciones del modelo que no son columnas
    class Meta:
        # Nombre singular y plural que muestra el Panel de Django (si no, diría "Posts")
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        # Orden por defecto: más recientes primero (evita el aviso de lista sin orden del Paginator)
        # El "-" indica descendente. Sin esto el orden queda a criterio de la BD y Paginator lanza
        # UnorderedObjectListWarning (las páginas podrían repetir o saltarse publicaciones).
        ordering = ['-created']

    # Texto con que se representa cada objeto (listado del admin, shell, etc.).
    # Sin __str__ el admin mostraría "Post object (1)".
    def __str__(self):
        return self.title
