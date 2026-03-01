from django import forms

from longclaw.shipping.models import ShippingRate


class CheckoutForm(forms.Form):
    """
    Captures extra info required for checkout
    """
    email = forms.EmailField()
    shipping_option = forms.ModelChoiceField(queryset=ShippingRate.objects.all(), empty_label=None)
    different_billing_address = forms.BooleanField(required=False)
    class Media:
        js = ('checkout.js',)
