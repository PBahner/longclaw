# orders/forms.py
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.widgets import AdminDateTimeInput
from wagtail.snippets.widgets import AdminSnippetChooser

from .models import Order, Address
from ..shipping.wagtail_hooks import AddressViewSet


class OrderAdminForm(WagtailAdminModelForm):
    class Meta:
        model = Order
        fields = [
            "status",
            "payment_date",
            "status_note",
            "shipping_rate",
            "shipping_address",
            "billing_address",
        ]
        widgets = {
            "payment_date": AdminDateTimeInput(),
            "shipping_address": AdminSnippetChooser(Address, icon=AddressViewSet.icon),
            "billing_address": AdminSnippetChooser(Address, icon=AddressViewSet.icon),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].disabled = True
        self.fields["payment_date"].disabled = True
