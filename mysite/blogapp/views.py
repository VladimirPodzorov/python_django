from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticlesListView(ListView):
    template_name = 'blogapp/article_list.html'
    queryset = (
        Article.objects.select_related("author", "category").prefetch_related("tags").defer("content")
    )


