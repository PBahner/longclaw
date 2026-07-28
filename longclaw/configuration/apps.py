from django.apps import AppConfig


class LongclawSettingsConfig(AppConfig):
    name = 'longclaw.configuration'
    label = 'longclaw_configuration'
    verbose_name = "Longclaw Configuration"
    default_auto_field = 'django.db.models.BigAutoField'
