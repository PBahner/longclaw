from datetime import datetime
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _, pgettext_lazy as _p
from longclaw.configuration.models import Configuration
from longclaw.settings import PRODUCT_VARIANT_MODEL
from longclaw.shipping.models import Address
from wagtail.models import Site

class Order(models.Model):
    SUBMITTED = 1
    FULFILLED = 2
    CANCELLED = 3
    REFUNDED = 4
    FAILURE = 5
    ORDER_STATUSES = ((SUBMITTED, _p("order_status", "Submitted")),
                      (FULFILLED, _p("order_status", "Fulfilled")),
                      (CANCELLED, _p("order_status", "Cancelled")),
                      (REFUNDED, _p("order_status", "Refunded")),
                      (FAILURE, _p("order_status", "Payment Failed")))
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Payment date"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date"))
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED, verbose_name=_("Status"))
    status_note = models.CharField(max_length=128, blank=True, null=True, verbose_name=_("Status note"))
    stock_updated = models.BooleanField(default=False, verbose_name=_("Stock updated"))

    transaction_id = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("Transaction ID"))

    # contact info
    email = models.EmailField(max_length=128, blank=True, null=True, verbose_name=_("Email"))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("IP address"))

    # shipping info
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_shipping_address", on_delete=models.PROTECT,
        verbose_name=_("Shipping address"),
    )

    # billing info
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, related_name="orders_billing_address", on_delete=models.PROTECT,
        verbose_name=_("Billing address"),
    )

    shipping_rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_("Shipping rate"),
    )

    def __str__(self):
        return _("Order #{order_id} - {email}").format(order_id=self.id, email=self.email)

    @property
    def total(self):
        """Total cost of the order
        """
        total = 0
        for item in self.items.all():
            total += item.total
        return total

    @property
    def total_items(self):
        """The number of individual items on the order
        """
        total = 0
        for item in self.items.all():
            total += item.quantity
        return total


    def refund(self):
        """Issue a full refund for this order
        """
        from longclaw.utils import GATEWAY
        now = datetime.strftime(datetime.now(), "%b %d %Y %H:%M:%S")
        if GATEWAY.issue_refund(self.transaction_id, self.total):
            self.status = self.REFUNDED
            self.status_note = _("Refunded on {}").format(now)
            self.increase_stock()
        else:
            self.status_note = _("Refund failed on {}").format(now)
        self.save()

    def fulfill(self):
        """Mark this order as being fulfilled
        """
        self.status = self.FULFILLED
        self.decrease_stock()
        self.save()

    def cancel(self, refund=True):
        """Cancel this order, optionally refunding it
        """
        if refund:
            self.refund()
        self.status = self.CANCELLED
        self.increase_stock()
        self.save()

    def decrease_stock(self):
        site = Site.objects.get(is_default_site=True)
        configuration = Configuration.for_site(site)
        if self.stock_updated or not configuration.enable_automatic_stock:
            return
        for item in self.items.all():
            product = item.product
            product.stock = F('stock') - item.quantity
            product.save()
        self.stock_updated = True

    def increase_stock(self):
        site = Site.objects.get(is_default_site=True)
        configuration = Configuration.for_site(site)
        if not self.stock_updated or not configuration.enable_automatic_stock:
            return
        for item in self.items.all():
            product = item.product
            product.stock = F('stock') + item.quantity
            product.save()
        self.stock_updated = False

    class Meta:
        permissions = [
            ("fulfill_order", _("Can fulfill orders")),
            ("cancel_order", _("Can cancel orders")),
            ("refund_order", _("Can refund orders")),
        ]
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class OrderItem(models.Model):
    product = models.ForeignKey(PRODUCT_VARIANT_MODEL, on_delete=models.DO_NOTHING, verbose_name=_("Product"))
    quantity = models.IntegerField(default=1, verbose_name=_("Quantity"))
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name=_("Order"))

    @property
    def total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{} x {}".format(self.quantity, self.product.get_product_title())

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
