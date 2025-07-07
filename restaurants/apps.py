from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    """
    AppConfig for the restaurants app, configuring app-specific settings and metadata.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'
