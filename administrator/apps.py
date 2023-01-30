from django.apps import AppConfig


class AdministratorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "administrator"

    def ready(self):
        from . import signals

        return super().ready()
