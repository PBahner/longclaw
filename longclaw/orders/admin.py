# longclaw/orders/admin.py
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, re_path, path
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from wagtail.admin import messages

from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.admin.viewsets.base import ViewSet

from longclaw.orders.models import Order
from longclaw.orders.views import OrderListView, OrderDetailView


class FulfillOrderView(PermissionRequiredMixin, View):
    permission_required = "longclaw_orders.fulfill_order"
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to fulfill orders.")
        return redirect(reverse("orders:list"))

    def get(self, request, pk, *args, **kwargs):
        return self.post(request, pk, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)

        try:
            order.fulfill()
            messages.success(request, f"Order #{order.pk} has been fulfilled.")
        except Exception as exc:
            messages.error(request, f"Failed to fulfill order #{order.pk}: {exc}")

        return redirect(reverse("orders:list"))


class CancelOrderView(PermissionRequiredMixin, View):
    permission_required = "longclaw_orders.cancel_order"
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to cancel orders.")
        return redirect(reverse("orders:list"))

    def get(self, request, pk, *args, **kwargs):
        return self.post(request, pk, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)

        try:
            order.cancel()
            messages.success(request, f"Order #{order.pk} has been cancelled.")
        except Exception as exc:
            messages.error(request, f"Failed to cancel order #{order.pk}: {exc}")

        return redirect(reverse("orders:list"))


class RefundOrderView(PermissionRequiredMixin, View):
    permission_required = "longclaw_orders.refund_order"
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to refund orders.")
        return redirect(reverse("orders:list"))

    def get(self, request, pk, *args, **kwargs):
        return self.post(request, pk, *args, **kwargs)

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)

        try:
            order.refund()
            messages.success(request, f"Order #{order.pk} has been refunded.")
        except Exception as exc:
            messages.error(request, f"Failed to refund order #{order.pk}: {exc}")

        return redirect(reverse("orders:list"))


class OrderViewSet(ViewSet):
    model = Order
    icon = "list-ul"
    menu_label = "Orders"
    menu_order = 100
    add_to_admin_menu = True

    def get_urlpatterns(self):
        urlpatterns = super().get_urlpatterns()
        urlpatterns += [
            path("", OrderListView.as_view(), name="list"),
            # add a detail URLs visible at: /admin/<model_name>/<pk>/
            path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
            re_path(r"^(?P<pk>\d+)/fulfill/$", FulfillOrderView.as_view(), name="fulfill"),
            re_path(r"^(?P<pk>\d+)/cancel/$", CancelOrderView.as_view(), name="cancel"),
            re_path(r"^(?P<pk>\d+)/refund/$", RefundOrderView.as_view(), name="refund"),
        ]
        return urlpatterns
