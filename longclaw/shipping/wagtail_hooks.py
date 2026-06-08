from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import SubmenuMenuItem, Menu, MenuItem
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from longclaw.configuration.models import Configuration
from longclaw.shipping.models import ShippingRate, Country, Address


class AddressViewSet(SnippetViewSet):
    model = Address
    icon = "form"
    menu_label = _("Addresses")
    menu_order = 210
    add_to_admin_menu = True
    list_display = ("name", "line_1", "line_2", "city", "postcode", "country")


class ShippingRateViewSet(SnippetViewSet):
    model = ShippingRate
    icon = "site"
    menu_label = _("Shipping Rates")
    menu_order = 220
    add_to_admin_menu = True
    list_display = ("name", "rate", "carrier", "description")


class CountryViewSet(SnippetViewSet):
    model = Country
    icon = "globe"
    menu_label = _("Shipping Countries")
    menu_order = 230
    add_to_admin_menu = True
    list_display = ("iso", "name_official", "name")


register_snippet(AddressViewSet)
register_snippet(ShippingRateViewSet)
register_snippet(CountryViewSet)


@hooks.register("construct_main_menu")
def register_shop_menu(request, menu_items):
    user = request.user

    def can_view_any(user, app_label, model):
        perms = [f"{app_label}.add_{model}", f"{app_label}.change_{model}", f"{app_label}.delete_{model}"]
        return any(user.has_perm(p) for p in perms)

    can_view_config = can_view_any(user, "longclaw_configuration", "configuration")
    can_view_shipping = can_view_any(user, "longclaw_shipping", "shippingrate")
    can_view_country = can_view_any(user, "longclaw_shipping", "country")
    can_view_address = can_view_any(user, "longclaw_shipping", "address")

    if not (can_view_config or can_view_shipping or can_view_country or can_view_address):
        return

    submenu_items = []

    if can_view_config:
        config_edit_url = reverse(
            "wagtailsettings:edit",
            args=[Configuration._meta.app_label, Configuration._meta.model_name]
        )
        submenu_items.append(
            MenuItem(
                _("General"),
                config_edit_url,
                icon_name="cog"
            ),
        )

    if can_view_address:
        address_list_url = reverse(AddressViewSet().get_url_name("list"))
        submenu_items.append(
            MenuItem(AddressViewSet.menu_label, address_list_url, icon_name=AddressViewSet.icon),
        )

    if can_view_shipping:
        shipping_list_url = reverse(ShippingRateViewSet().get_url_name("list"))
        submenu_items.append(
            MenuItem(ShippingRateViewSet.menu_label, shipping_list_url, icon_name=ShippingRateViewSet.icon),
        )

    if can_view_country:
        country_list_url = reverse(CountryViewSet().get_url_name("list"))
        submenu_items.append(
            MenuItem(CountryViewSet.menu_label, country_list_url, icon_name=CountryViewSet.icon),
        )

    if submenu_items:
        menu_items.append(
            SubmenuMenuItem(
                _("Shop Settings"),
                Menu(items=submenu_items),
                icon_name="cogs",
                order=10000,
            )
        )


@hooks.register("construct_settings_menu")
def hide_my_settings(request, menu_items):
    config_label = Configuration._meta.verbose_name
    menu_items[:] = [
        item for item in menu_items
        if item.label != config_label
    ]


@hooks.register("construct_main_menu")
def hide_my_snippets_from_menu(request, menu_items):
    items_to_hide = {
        ShippingRateViewSet.menu_label,
        CountryViewSet.menu_label,
        AddressViewSet.menu_label
    }
    menu_items[:] = [
        item for item in menu_items
        if item.label not in items_to_hide
    ]
