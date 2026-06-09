from django.urls import reverse, path
from wagtail import hooks
from wagtail.admin.menu import MenuItem

from longclaw.products.views import ProductStockReportView


class ProductStockReportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm(ProductStockReportView.permission)

@hooks.register('register_reports_menu_item')
def register_product_stock_report_menu_item():
    return ProductStockReportMenuItem(
        ProductStockReportView.page_title,
        reverse('product_stock_report'),
        icon_name=ProductStockReportView.header_icon,
        order=1500
    )

@hooks.register('register_admin_urls')
def register_product_stock_report_url():
    return [
        path('reports/product-stock/', ProductStockReportView.as_view(), name='product_stock_report'),
        path('reports/product-stock/results/', ProductStockReportView.as_view(results_only=True), name='product_stock_report_results'),
    ]
