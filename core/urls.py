from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path(
        "journalist/dashboard/",
        views.journalist_dashboard_view,
        name="journalist_dashboard",
    ),

    path("articles/", views.article_list_view, name="article_list"),
    path(
        "articles/<int:article_id>/",
        views.article_detail_view,
        name="article_detail",
    ),

    path("newsletters/", views.newsletter_list_view, name="newsletter_list"),
    path(
        "newsletters/<int:newsletter_id>/",
        views.newsletter_detail_view,
        name="newsletter_detail",
    ),

    path(
        "editor/articles/",
        views.editor_article_list_view,
        name="editor_article_list",
    ),
    path(
        "editor/articles/<int:article_id>/approve/",
        views.approve_article_view,
        name="approve_article",
    ),

    path(
        "journalist/articles/create/",
        views.create_article_view,
        name="create_article",
    ),
    path(
        "journalist/articles/<int:article_id>/edit/",
        views.update_article_view,
        name="update_article",
    ),
    path(
        "journalist/articles/<int:article_id>/delete/",
        views.delete_article_view,
        name="delete_article",
    ),

    path(
        "journalist/newsletters/create/",
        views.create_newsletter_view,
        name="create_newsletter",
    ),
    path(
        "journalist/newsletters/<int:newsletter_id>/edit/",
        views.update_newsletter_view,
        name="update_newsletter",
    ),
    path(
        "journalist/newsletters/<int:newsletter_id>/delete/",
        views.delete_newsletter_view,
        name="delete_newsletter",
    ),

    path(
        "editor/publishers/create/",
        views.create_publisher_view,
        name="create_publisher",
    ),

    path(
        "subscribe/publisher/<int:publisher_id>/",
        views.subscribe_publisher_view,
        name="subscribe_publisher",
    ),
    path(
        "unsubscribe/publisher/<int:publisher_id>/",
        views.unsubscribe_publisher_view,
        name="unsubscribe_publisher",
    ),
    path(
        "subscribe/journalist/<int:journalist_id>/",
        views.subscribe_journalist_view,
        name="subscribe_journalist",
    ),
    path(
        "unsubscribe/journalist/<int:journalist_id>/",
        views.unsubscribe_journalist_view,
        name="unsubscribe_journalist",
    ),
]