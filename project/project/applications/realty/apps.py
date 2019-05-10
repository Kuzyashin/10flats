from django.apps import AppConfig


class RealtyConfig(AppConfig):
    name = 'realty'

    def ready(self):
        import realty.signals