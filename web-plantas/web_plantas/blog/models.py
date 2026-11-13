from django.db import models
# now: función que devuelve la fecha y hora actual. Se pasa SIN paréntesis como default,
# así Django la llama cada vez que se crea un Post (con paréntesis quedaría fija la hora de arranque del servidor).
from django.utils.timezone import now


# Modelo Category: tabla blog_category. Las categorías se crean desde el Panel de Django.
# Se relaciona con Post por ManyToMany: un post puede tener varias categorías y una categoría varios posts.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        # Orden alfabético en el admin y en la lista lateral del blog
        ordering = ['name']

    # Sin __str__ el selector de categorías del admin mostraría "Category object (1)"
    def __str__(self):
        return self.name


# Modelo Author: tabla blog_author. Reemplaza el autor que antes era texto libre en Post.
# Se relaciona con Post por ForeignKey (uno a muchos): un autor escribe muchos posts, cada post tiene un autor.
class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    specialty = models.CharField(max_length=150, verbose_name="Especialidad")
    # blank=True: la foto es opcional en el formulario del admin (sin esto sería obligatoria)
    photo = models.ImageField(upload_to="authors", blank=True, verbose_name="Foto")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['name']

    # Es lo que se imprime con {{ p.author }} en la plantilla y en el desplegable de autores del admin
    def __str__(self):
        return self.name


# Modelo Post: cada clase que hereda de models.Model se convierte en una tabla de la BD (blog_post).
# Cada atributo = una columna. Django agrega solo la columna "id" (clave primaria autoincremental).
# Después de cambiar algo aquí hay que correr: makemigrations (crea el archivo) y migrate (lo aplica a la BD).
class Post(models.Model):
    # CharField: texto corto, max_length es obligatorio (VARCHAR). verbose_name = etiqueta en el admin
    title = models.CharField(max_length=200, verbose_name="Título")
    subtitle = models.CharField(max_length=200, verbose_name="Subtítulo")
    # TextField: texto largo sin límite de caracteres
    content = models.TextField(verbose_name="Contenido")
    # ForeignKey: guarda en la columna author_id el id de un Author (en el admin aparece como desplegable).
    # on_delete=CASCADE: si se borra el autor, se borran también sus publicaciones.
    # Sin on_delete Django no arranca (es obligatorio).
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Autor")
    # ManyToManyField: Django crea una tabla intermedia (blog_post_categories) con pares post_id / category_id.
    # Desde una categoría se llega a sus posts con category.post_set.all (lo usa category.html).
    categories = models.ManyToManyField(Category, verbose_name="Categorías")
    # ImageField: guarda en la BD solo la ruta del archivo; la imagen física va a MEDIA_ROOT/blog/.
    # Requiere Pillow instalado (si no, makemigrations da error). Es obligatorio al no tener blank=True.
    image = models.ImageField(upload_to="blog", verbose_name="Imagen")
    # Fecha que se muestra en el sitio. A diferencia de created, se puede editar (ej. programar una fecha).
    published = models.DateTimeField(default=now, verbose_name="Fecha de publicación")
    # auto_now_add: se llena una sola vez, al crear el registro (no se puede editar en el admin)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    # auto_now: se actualiza con la fecha actual cada vez que se guarda (save) el registro
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    # Meta: opciones del modelo que no son columnas
    class Meta:
        # Nombre singular y plural que muestra el Panel de Django (si no, diría "Posts")
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        # Orden por defecto: más recientes primero según la fecha de publicación.
        # El "-" indica descendente. Sin esto el orden queda a criterio de la BD y Paginator lanza
        # UnorderedObjectListWarning (las páginas podrían repetir o saltarse publicaciones).
        ordering = ['-published']

    # Texto con que se representa cada objeto (listado del admin, shell, etc.).
    # Sin __str__ el admin mostraría "Post object (1)".
    def __str__(self):
        return self.title
