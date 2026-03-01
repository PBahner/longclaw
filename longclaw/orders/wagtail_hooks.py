from django.contrib.auth.models import Permission
from wagtail import hooks

from longclaw.orders.admin import OrderViewSet


@hooks.register('register_permissions')
def register_permissions():
    app = 'longclaw_orders'
    model = 'order'

    return Permission.objects.filter(content_type__app_label=app, codename__in=[
        # f"add_{model}",
        f"change_{model}",
        # f"delete_{model}",
        f"fulfill_{model}",
        f"cancel_{model}",
        f"refund_{model}",
    ])

@hooks.register("construct_main_menu")
def hide_orders_menu_for_restricted_users(request, menu_items):
    user = request.user

    # Only show Orders menu if user has at least one relevant permission
    can_access_orders = any(
        user.has_perm(f"longclaw_orders.{perm}")
        for perm in ["change_order", "fulfill_order", "cancel_order", "refund_order"]
    )

    if not can_access_orders:
        # Remove the Orders menu item if it exists
        menu_items[:] = [
            item for item in menu_items
            if getattr(item, "label", "") != "Orders"
        ]


@hooks.register("register_admin_viewset")
def register_orders_viewset():
    return OrderViewSet("orders")
