"""
Admin configuration for the News Portal application.

This module registers models with the Django admin interface
and customizes their display.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Publisher, Article, Newsletter


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for User model.
    """

    model = User

    list_display = (
        "username",
        "email",
        "role",
        "is_staff",
        "is_superuser",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Role and Subscriptions", {
            "fields": (
                "role",
                "subscribed_publishers",
                "subscribed_journalists",
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role and Subscriptions", {
            "fields": (
                "role",
                "subscribed_publishers",
                "subscribed_journalists",
            )
        }),
    )


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    """Admin view for Publisher model."""

    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin view for Article model."""

    list_display = ("title", "author", "publisher", "approved", "created_at")
    list_filter = ("approved", "publisher", "created_at")
    search_fields = ("title", "content")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin view for Newsletter model."""

    list_display = ("title", "author", "created_at")
    search_fields = ("title", "description")