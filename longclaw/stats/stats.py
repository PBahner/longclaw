"""
Various stats/analysis calculations
"""
import itertools
import calendar
from datetime import date
from django.db.models import Q, Sum, F, QuerySet
from django.utils import timezone

from longclaw.orders.models import Order, OrderItem


def current_month() -> tuple[date, date]:
    now = timezone.localdate()
    month_start = now.replace(day=1)
    month_end = now.replace(day=calendar.monthrange(now.year, now.month)[1])
    return month_start, month_end


def sales_for_time_period(from_date: date, to_date: date) -> QuerySet:
    """
    Get all sales for a given time period
    """
    sales = Order.objects.filter(
        Q(payment_date__date__lte=to_date) & Q(payment_date__date__gte=from_date)
    ).exclude(status=Order.CANCELLED)

    return sales


def daily_sales(from_date: date, to_date: date) -> itertools.groupby:
    sales = sales_for_time_period(from_date, to_date)
    grouped = itertools.groupby(sales, lambda order: order.payment_date.strftime("%Y-%m-%d"))
    return grouped

def sales_by_product(from_date: date, to_date: date) -> QuerySet:
    sales = OrderItem.objects.filter(
        Q(order__payment_date__date__lte=to_date) & Q(order__payment_date__date__gte=from_date)
    ).exclude(
        order__status=Order.CANCELLED
    ).annotate(
        title=F('product__product__title')
    ).values(
        'title'
    ).annotate(
        quantity=Sum('quantity')
    ).order_by('-quantity')

    return sales
