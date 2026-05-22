from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from longclaw.configuration.models import Configuration
from longclaw.shipping.models import Address, Country

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'line_1', 'line_2', 'city', 'postcode', 'country']
        labels = {
            'name': _('Name'),
            'line_1': _('Line 1'),
            'line_2': _('Line 2'),
            'city': _('City'),
            'postcode': _('Postcode'),
            'country': _('Country'),
        }

    def __init__(self, *args, **kwargs):
        site = kwargs.pop('site', None)
        super(AddressForm, self).__init__(*args, **kwargs)

        # Edit the country field to only contain
        # countries specified for shipping
        all_countries = True
        if site:
            settings = Configuration.for_site(site)
            all_countries = settings.default_shipping_enabled
        if all_countries:
            queryset = Country.objects.all()
        else:
            queryset = Country.objects.exclude(shippingrate=None)
        self.fields['country'] = ModelChoiceField(label=_('Country'), queryset=queryset, empty_label=None)

