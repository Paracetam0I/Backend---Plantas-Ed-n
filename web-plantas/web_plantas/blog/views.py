from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post  # "." = importa desde la misma app (blog/models.py)


# Vista basada en función: recibe la petición (request) y devuelve una respuesta HTML
def blog(request):
    # QuerySet con todas las publicaciones, ya ordenadas por Meta.ordering (-created).
    # Es "perezoso": la consulta SQL no se ejecuta aquí, sino cuando el Paginator pide sus filas.
    posts = Post.objects.all()
    # Paginación: 3 publicaciones por página
    # Con 10 publicaciones quedan 4 páginas (3 + 3 + 3 + 1). Cambiar el 3 cambia cuántas se ven.
    paginator = Paginator(posts, 3)
    # Lee el número de página de la URL: /blog/?page=2 -> "2". Si no viene, queda None
    page_number = request.GET.get("page")
    # get_page() es tolerante a errores: None o texto ("abc") -> página 1;
    # número mayor al total (99) -> última página. Así nunca da error 404.
    # Devuelve un objeto Page: se recorre como lista y trae has_next, number, paginator, etc.
    posts = paginator.get_page(page_number)
    # render() une la plantilla con el contexto (diccionario) y devuelve el HttpResponse.
    # La clave 'posts' es el nombre de la variable dentro de blog.html.
    # Sin paginación se podría pasar Post.objects.all() directo y se mostrarían todas juntas.
    return render(request, "blog/blog.html", {'posts': posts})
