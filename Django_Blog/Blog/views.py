from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Article
from .models import Category
from .utils import busqueda_articulos_por_categoria
from django.contrib import messages
from .models import Comment
from django.core.paginator import Paginator

def category_view(request, slug):
    categoria = Category.objects.get(slug = slug)
    articulos = Article.objects.filter(category = categoria, state = True).order_by('-id_article')

    # Paginacion por cada 5 articulos
    paginacion = Paginator(articulos, 1)
    num_pagina = request.GET.get('page')
    articulos = paginacion.get_page(num_pagina)

    if request.GET.get('q'):
        parametro_busqueda = request.GET.get('q')

        if len(busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)) == 0:
            messages.error(request, f'No se encontraron coincidencias con {parametro_busqueda}')
        else:
            articulos = busqueda_articulos_por_categoria(request, parametro_busqueda, categoria)

    return render(request, 'blog/detalle-categoria.html', context = {
        'categoria': categoria,
        'articulos': articulos,
        'paginacion': paginacion
    })



class ArticleDetailView(DetailView):
    template_name = 'blog/detalle-articulo.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulo'] = context['object']
        context['comentarios'] = Comment.objects.filter(article = context['articulo']).order_by('-modified')

        return context