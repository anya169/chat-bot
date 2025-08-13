from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    def ready(self):
        # При импорте моделей Django автоматически зарегистрирует сигналы
        import core.signals
