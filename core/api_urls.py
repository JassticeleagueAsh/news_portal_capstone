from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import (
    ArticleCreateAPIView,
    ArticleDeleteAPIView,
    ArticleDetailAPIView,
    ArticleListAPIView,
    ArticleUpdateAPIView,
    SubscribedArticleListAPIView,
)

urlpatterns = [
    path("articles/", ArticleListAPIView.as_view(), name="api_article_list"),
    path(
        "articles/subscribed/",
        SubscribedArticleListAPIView.as_view(),
        name="api_subscribed_articles",
    ),
    path("articles/<int:pk>/", ArticleDetailAPIView.as_view(), name="api_article_detail"),
    path("articles/create/", ArticleCreateAPIView.as_view(), name="api_article_create"),
    path(
        "articles/<int:pk>/update/",
        ArticleUpdateAPIView.as_view(),
        name="api_article_update",
    ),
    path(
        "articles/<int:pk>/delete/",
        ArticleDeleteAPIView.as_view(),
        name="api_article_delete",
    ),
    path("token/", obtain_auth_token, name="api_token"),
]