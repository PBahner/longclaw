from django import forms
from django.utils.translation import gettext as _

from longclaw.shipping.models import ShippingRate


class CheckoutForm(forms.Form):
    """
    Captures extra info required for checkout
    """
    email = forms.EmailField(label=_('Email'))
    shipping_option = forms.ModelChoiceField(
        label=_('Shipping Option'),
        queryset=ShippingRate.objects.all(),
        required=False,
        empty_label=None
    )
    different_billing_address = forms.BooleanField(label=_('Different Billing Address'), required=False)
    customer_note = forms.CharField(label=_('Notes'), required=False, widget=forms.Textarea(attrs={'rows': 4}))
    class Media:
        js = ('checkout.js',)
