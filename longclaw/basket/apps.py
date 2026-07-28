from django.apps import AppConfig


class BasketConfig(AppConfig):
    name = 'longclaw.basket'
    label = 'longclaw_basket'
    verbose_name = "Longclaw Basket"
    default_auto_field = 'django.db.models.BigAutoField'
