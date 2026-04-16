from django.apps import AppConfig

"""
Application configuration for the core app.

Ensures signals are registered when the app is ready.
"""


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals