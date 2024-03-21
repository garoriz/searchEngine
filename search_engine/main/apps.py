from django.apps import AppConfig

from . import engine


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        engine.load_vectors()
