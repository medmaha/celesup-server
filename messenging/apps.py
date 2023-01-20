from django.apps import AppConfig


class MessengingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messenging"

    def ready(self) -> None:
        from . import signals

        return super().ready()
