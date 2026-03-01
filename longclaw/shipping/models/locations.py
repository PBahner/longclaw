from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable


class Address(models.Model):
    name = models.CharField(max_length=64)
    line_1 = models.CharField(max_length=128)
    line_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=10)
    country = models.ForeignKey('longclaw_shipping.Country', blank=True, null=True, on_delete=models.PROTECT)

    panels = [
        FieldPanel('name'),
        FieldPanel('line_1'),
        FieldPanel('line_2'),
        FieldPanel('city'),
        FieldPanel('postcode'),
        FieldPanel('country')
    ]

    def __str__(self):
        if self.line_2:
            return "{}, {}, {}, {}, {}, {}".format(self.name, self.line_1, self.line_2, self.postcode, self.city, self.country)
        else:
            return "{}, {}, {}, {}, {}".format(self.name, self.line_1, self.postcode, self.city, self.country)


class Country(Orderable):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    Instance Variables:
    iso -- ISO 3166-1 alpha-2
    name -- Official country names (in all caps) used by the ISO 3166
    display_name -- Country names in title format
    sort_priority -- field that allows for customizing the default ordering
    0 is the default value, and the higher the value the closer to the
    beginning of the list it will be.  An example use case would be you will
    primarily have addresses for one country, so you want that particular
    country to be the first option in an html dropdown box.  To do this, you
    would simply change the value in the json file or alter
    country_grabber.py's priority dictionary and run it to regenerate
    the json
    """
    iso = models.CharField(max_length=2, primary_key=True)
    name_official = models.CharField(max_length=128)
    name = models.CharField(max_length=128)

    panels = [
        FieldPanel('iso'),
        FieldPanel('name_official'),
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        """ Return the display form of the country name"""
        return self.name
