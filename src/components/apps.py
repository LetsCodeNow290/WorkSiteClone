from django.apps import AppConfig


class ComponentsConfig(AppConfig):
    name = 'components'

    def ready(self):
        import components.signals