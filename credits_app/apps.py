from django.apps import AppConfig


class CreditsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'credits_app'
    verbose_name = 'Crédits'

    def ready(self):
        import credits_app.signals  # noqa: F401
