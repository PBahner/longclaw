from django.forms import ModelForm, ModelChoiceField
from django.utils.translation import gettext as _
from longclaw.configuration.models import Configuration
from longclaw.shipping.models import Address, Country

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'line_1', 'line_2', 'city', 'postcode', 'country']

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

    def save(self, commit=True):
        """
        override the default save method to check if an address with the same details already exists,
        and if so return that instead of creating a new one
        """

        cleaned = self.cleaned_data

        lookup = dict(
            name=cleaned["name"],
            line_1=cleaned["line_1"],
            line_2=cleaned.get("line_2", ""),
            city=cleaned["city"],
            postcode=cleaned["postcode"],
            country=cleaned.get("country"),
        )

        instance, created = Address.objects.get_or_create(**lookup)

        return instance

