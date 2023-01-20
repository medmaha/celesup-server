from django.apps import AppConfig

import threading


class HashtagsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hashtags"

    def ready(self):
        from . import signals

        # from utilities import createFakeObjects

        # threading.Thread(target=run, args=(createFakeObjects,))
        # run(createFakeObjects)
        return super().ready()


def run(createFakeObjects):
    # createFakeObjects.createFakeUsers()
    # createFakeObjects.createFakePost()

    return True
