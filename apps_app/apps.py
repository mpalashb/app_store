from django.apps import AppConfig


class AppsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps_app'

    def ready(self):
        import apps_app.signals
