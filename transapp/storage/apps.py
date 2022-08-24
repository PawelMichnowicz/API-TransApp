from django.apps import AppConfig


class StorageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from . import signals
        # # Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback)