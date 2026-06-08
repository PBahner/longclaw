"""
Admin configurable settings for longclaw apps
"""
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.utils.translation import gettext_lazy as _

from longclaw.shipping.models import Address


@register_setting
class Configuration(BaseSiteSetting):
    default_shipping_rate = models.DecimalField(
        default=3.95,
        max_digits=12,
        decimal_places=2,
        verbose_name=_("Default shipping rate"),
        help_text=_("The default shipping rate for countries which have not been configured")
    )
    default_shipping_carrier = models.CharField(
        default="Royal Mail",
        max_length=32,
        verbose_name=_("Default shipping carrier"),
        help_text=_("The default shipping carrier")
    )
    default_shipping_enabled = models.BooleanField(
        default=False,
        verbose_name=_("Default shipping enabled"),
        help_text=_(
            "Whether to enable default shipping. "
            "This essentially means you ship to all countries, "
            "not only those with configured shipping rates"
        )
    )

    shipping_origin = models.ForeignKey(
        Address,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_("Shipping origin"),
    )

    currency_html_code = models.CharField(
        max_length=12,
        default="&pound;",
        verbose_name=_("Currency HTML code"),
        help_text=_("The HTML code for the currency symbol. Used for display purposes only")
    )
    currency = models.CharField(
        max_length=6,
        default="GBP",
        verbose_name=_("Currency"),
        help_text=_("The iso currency code to use for payments")
    )

    enable_automatic_stock = models.BooleanField(
        default=True,
        verbose_name=_("Enable automatic stock"),
        help_text=_("If this is enabled, the products stock will automatically be updated when an order is placed.")
    )

    panels = (
        FieldPanel('default_shipping_rate'),
        FieldPanel('default_shipping_carrier'),
        FieldPanel('default_shipping_enabled'),
        FieldPanel('shipping_origin'),
        FieldPanel('currency_html_code'),
        FieldPanel('currency'),
        FieldPanel('enable_automatic_stock'),
    )

    class Meta:
        verbose_name = _("Shop Configuration")
