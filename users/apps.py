from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    # ** When using seperate signals.py file
    # use this function to allow django
    # to connect to the signals.py file
    def ready(self):
        import users.signals

