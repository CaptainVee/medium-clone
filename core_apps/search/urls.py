from django.urls import path
from .views import ArticleElasticSearchView


urlpatterns = [
    path(
        "",
        ArticleElasticSearchView.as_view({"get": "list"}),
        name="article-search",
    ),
]
