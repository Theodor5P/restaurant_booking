from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    AppConfig for the users app, configuring app-specific settings and metadata.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
