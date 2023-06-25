from django.urls import path

from .views import ArticlesListView

app_name = 'blogapp'
urlpatterns = [
    path('blog-list/', ArticlesListView.as_view(), name='articles_list'),
]
