from django.core.paginator import Paginator
# get_object_or_404: busca un objeto y, si no existe, responde 404 en vez de lanzar DoesNotExist (error 500)
from django.shortcuts import render, get_object_or_404
from .models import Post, Category  # "." = importa desde la misma app (blog/models.py)


# Vista basada en función: recibe la petición (request) y devuelve una respuesta HTML
def blog(request):
    # QuerySet con todas las publicaciones, ya ordenadas por Meta.ordering (-published).
    # Es "perezoso": la consulta SQL no se ejecuta aquí, sino cuando el Paginator pide sus filas.
    posts = Post.objects.all()
    # Paginación: 3 publicaciones por página
    # Con 11 publicaciones quedan 4 páginas (3 + 3 + 3 + 2). Cambiar el 3 cambia cuántas se ven.
    paginator = Paginator(posts, 3)
    # Lee el número de página de la URL: /blog/?page=2 -> "2". Si no viene, queda None
    page_number = request.GET.get("page")
    # get_page() es tolerante a errores: None o texto ("abc") -> página 1;
    # número mayor al total (99) -> última página. Así nunca da error 404.
    # Devuelve un objeto Page: se recorre como lista y trae has_next, number, paginator, etc.
    posts = paginator.get_page(page_number)
    # Todas las categorías, para la lista de enlaces de la barra lateral.
    # Así una categoría nueva creada en el panel aparece sola, sin tocar la plantilla.
    categories = Category.objects.all()
    # render() une la plantilla con el contexto (diccionario) y devuelve el HttpResponse.
    # Las claves 'posts' y 'categories' son los nombres de las variables dentro de blog.html.
    return render(request, "blog/blog.html", {'posts': posts, 'categories': categories})


# Vista de una categoría. category_id llega desde la URL: /category/2/ -> category_id = "2"
# (el nombre del parámetro debe coincidir con <category_id> en urls.py, si no -> TypeError).
def category(request, category_id):
    # Busca la categoría por id; si no existe (ej. /category/99/) responde 404 "Página no encontrada".
    category = get_object_or_404(Category, id=category_id)
    # Solo se envía la categoría: sus posts se obtienen en la plantilla con category.post_set.all
    return render(request, "blog/category.html", {'category': category})
