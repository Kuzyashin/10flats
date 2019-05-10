from django.apps import AppConfig


class TypeformConfig(AppConfig):
    name = 'typeform'

    def ready(self):
        import typeform.signals