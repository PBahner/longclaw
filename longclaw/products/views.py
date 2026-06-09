from django.apps import apps
from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.reports import PageReportView
from wagtail.admin.auth import permission_denied
from wagtail.models import Page

from .models import ProductBase


class ProductStockReportView(PageReportView):
    page_title = _("Product Stock")
    index_url_name = "product_stock_report"
    index_results_url_name = "product_stock_report_results"
    results_template_name = "reports/product_stock_report_results.html"
    header_icon = "order"
    permission = "longclaw_configuration.change_configuration"

    def get_queryset(self):
        product_models = [
            model for model in apps.get_models()
            if issubclass(model, Page) and issubclass(model, ProductBase)
        ]

        rows = []
        for model in product_models:
            qs = model.objects.prefetch_related("variants").all().order_by("-live")
            for product in qs:
                for variant in product.variants.all():
                    product_copy = type(product).objects.get(pk=product.pk)
                    product_copy.variant = variant
                    rows.append(product_copy)

        return rows

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.has_perm(self.permission):
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)
