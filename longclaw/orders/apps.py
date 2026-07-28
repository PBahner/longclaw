from django.apps import AppConfig


class LongclawOrdersConfig(AppConfig):
    name = 'longclaw.orders'
    label = 'longclaw_orders'
    verbose_name = "Longclaw Orders"
    default_auto_field = 'django.db.models.BigAutoField'
