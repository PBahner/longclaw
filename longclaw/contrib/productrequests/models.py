from django.db import models
from django.utils.translation import gettext_lazy as _
from longclaw.settings import PRODUCT_VARIANT_MODEL

class ProductRequest(models.Model):
    variant = models.ForeignKey(
        PRODUCT_VARIANT_MODEL,
        related_name='requests',
        on_delete=models.CASCADE,
        verbose_name=_("Variant"),
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created date"),
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_("Email"),
        help_text=_("Optional email of the customer who made the request")
    )

    class Meta:
        verbose_name = _("Product Request")
        verbose_name_plural = _("Product Requests")
