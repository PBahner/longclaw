# orders/views.py
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.utils.translation import gettext_lazy as _
from wagtail.admin.messages import success
from wagtail.admin.views.generic import IndexView, WagtailAdminTemplateMixin
from wagtail.admin.ui.tables import Column, TitleColumn, StatusTagColumn, BulkActionsCheckboxColumn, ButtonsColumnMixin
from wagtail.admin.widgets import Button, ButtonWithDropdown

from .forms import OrderAdminForm
from .models import Order


class StatusColumn(StatusTagColumn):
    statuses = dict(Order.ORDER_STATUSES)

    def get_value(self, instance):
        value = super().get_value(instance)
        return self.statuses.get(value)


class OrderActionsColumn(ButtonsColumnMixin, TitleColumn):

    def get_buttons(self, instance, parent_context):
        user = parent_context["request"].user
        buttons = []
        list_buttons = []

        if user.has_perm("longclaw_orders.change_order"):
            buttons.append(
                Button(
                    label=_("Details"),
                    icon_name="edit",
                    url=reverse("orders:detail", args=[instance.pk]),
                    priority=40,
                    attrs={"title": _("Show order details")},
                )
            )
        if user.has_perm("longclaw_orders.cancel_order"):
            buttons.append(
                Button(
                    label=_("Cancel"),
                    icon_name="cross",
                    url=reverse("orders:cancel", args=[instance.pk]),
                    priority=50,
                    attrs={"title": _("Cancel this order")},
                )
            )
        if user.has_perm("longclaw_orders.fulfill_order"):
            buttons.append(
                Button(
                    label=_("Fulfill"),
                    icon_name="check",
                    url=reverse("orders:fulfill", args=[instance.pk]),
                    priority=60,
                    attrs={"title": _("Fulfill this order")},
                )
            )
        if user.has_perm("longclaw_orders.refund_order"):
            buttons.append(
                Button(
                    label=_("Refund"),
                    icon_name="expand-right",
                    url=reverse("orders:refund", args=[instance.pk]),
                    priority=70,
                    attrs={"title": _("Refund this order")},
                )
            )

        if not buttons:
            return list_buttons

        list_buttons.append(
            ButtonWithDropdown(
                buttons=buttons,
                icon_name="dots-horizontal",
                attrs={
                    "aria-label": _("More options for '%(title)s'")
                    % {"title": str(instance)},
                },
            )
        )
        return list_buttons


class OrderListView(PermissionRequiredMixin, IndexView):
    model = Order
    page_title = _("Orders")
    paginate_by = 25
    ordering = "-created_date"
    inspect_url_name = "orders:detail"
    edit_url_name = "orders:detail"
    delete_url_name = "orders:delete"
    # list_filter = ("status",)
    permission_required = []

    columns = [
        BulkActionsCheckboxColumn("bulk_actions", obj_type="snippet"),
        OrderActionsColumn(
            "id",
            label="ID",
            url_name="orders:detail",
            accessor=lambda o: f"#{o.id}",
        ),
        # OrderActionsColumn("actions"),
        StatusColumn("status", label=_("Status")),
        Column("status_note", label=_("Status note")),
        Column("shipping_address", label=_("Shipping address")),
        Column("created_date", label=_("Created date")),
        Column("payment_date", label=_("Payment date")),
        Column("shipping_rate", label=_("Shipping rate")),
        Column("total_items", label=_("Total items")),
        Column("total", label=_("Total")),
    ]

    def has_permission(self):
        return any(
            self.request.user.has_perm(f"longclaw_orders.{perm}")
            for perm in ["change_order", "fulfill_order", "cancel_order", "refund_order"]
        )


class OrderDetailView(PermissionRequiredMixin, WagtailAdminTemplateMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    page_title = _("Order details")
    permission_required = "longclaw_orders.change_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object

        context["items"] = order.items.select_related("product")
        context["form"] = OrderAdminForm(
            instance=order,
            data=self.request.POST or None,
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = OrderAdminForm(request.POST, instance=self.object)

        if form.is_valid():
            form.save()
            success(request, _("Order updated"))
            return redirect(request.path)

        return self.get(request, *args, **kwargs)

    def get_breadcrumbs_items(self):
        return self.breadcrumbs_items + [
            {"url": reverse_lazy("orders:list"), "label": _("Orders")},
            {"url": self.request.path, "label": self.object}
        ]

