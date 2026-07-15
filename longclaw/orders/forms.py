# orders/forms.py
from django.forms.widgets import Textarea
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.admin.widgets import AdminDateTimeInput
from wagtail.snippets.widgets import AdminSnippetChooser

from .models import Order, Address


class OrderAdminForm(WagtailAdminModelForm):
    class Meta:
        model = Order
        fields = [
            "status",
            "payment_date",
            "status_note",
            "customer_note",
            "shipping_rate",
            "shipping_address",
            "billing_address",
        ]
        widgets = {
            "payment_date": AdminDateTimeInput(),
            "customer_note": Textarea(attrs={"rows": 4}),
            "shipping_address": AdminSnippetChooser(Address, icon="form"),
            "billing_address": AdminSnippetChooser(Address, icon= "form"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].disabled = True
        self.fields["payment_date"].disabled = True
