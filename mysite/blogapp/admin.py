from django.contrib import admin

from blogapp.models import Article, Author, Category, Tag


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = 'name', 'bio'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'name',


class TagsInline(admin.TabularInline):
    model = Article.tags.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TagsInline,
    ]
    list_display = 'title', 'content', 'pub_date', 'author', 'category'

    def get_queryset(self, request):
        return Article.objects.select_related('author').prefetch_related('tags')
