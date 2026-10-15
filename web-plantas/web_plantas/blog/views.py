from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post


def blog(request):
    posts = Post.objects.all()
    # Paginación: 3 publicaciones por página
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, "blog/blog.html", {'posts': posts})
