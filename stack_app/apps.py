from django.apps import AppConfig


class StackAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stack_app'

    def ready(self):
        import stack_app.signals