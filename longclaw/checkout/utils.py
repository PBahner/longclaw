from decimal import Decimal
from django.utils import timezone
from django.utils.translation import gettext as _
from ipware import get_client_ip

from longclaw.basket.utils import get_basket_items, destroy_basket
from longclaw.shipping.utils import get_shipping_cost
from longclaw.checkout.errors import PaymentError
from longclaw.orders.models import Order, OrderItem
from longclaw.shipping.models import Address
from longclaw.configuration.models import Configuration
from longclaw.utils import GATEWAY


def create_order(email,
                 request,
                 phone_number=None,
                 customer_note=None,
                 addresses=None,
                 shipping_address=None,
                 billing_address=None,
                 shipping_option=None,
                 capture_payment=False):
    """
    Create an order from a basket and customer infomation
    """
    basket_items, current_basket_id = get_basket_items(request)
    if addresses:
        # Longclaw < 0.2 used 'shipping_name', longclaw > 0.2 uses a consistent
        # prefix (shipping_address_xxxx)
        try:
            shipping_name = addresses['shipping_name']
        except KeyError:
            shipping_name = addresses['shipping_address_name']

        shipping_country = addresses['shipping_address_country']
        if not shipping_country:
            shipping_country = None
        shipping_address, _created = Address.objects.get_or_create(
            name=shipping_name,
            line_1=addresses['shipping_address_line1'],
            city=addresses['shipping_address_city'],
            postcode=addresses['shipping_address_zip'],
            country=shipping_country
        )
        shipping_address.save()
        try:
            billing_name = addresses['billing_name']
        except KeyError:
            billing_name = addresses['billing_address_name']
        billing_country = addresses['shipping_address_country']
        if not billing_country:
            billing_country = None
        billing_address, _created = Address.objects.get_or_create(
            name=billing_name,
            line_1=addresses['billing_address_line1'],
            city=addresses['billing_address_city'],
            postcode=addresses['billing_address_zip'],
            country=billing_country
        )
        billing_address.save()
    else:
        shipping_country = shipping_address.country

    ip_address = get_client_ip(request)
    if shipping_country and shipping_option:
        site_settings = Configuration.for_request(request)
        shipping_rate = get_shipping_cost(
            site_settings,
            shipping_address.country.pk,
            shipping_option,
            basket_id=current_basket_id,
            destination=shipping_address,
        )['rate']
    else:
        shipping_rate = Decimal(0)

    # If the basket is empty this may be a duplicated request.
    # Try to find the existing order and return it.
    if not basket_items.exists():
        existing = Order.objects.filter(
            basket_id=current_basket_id,
            email=email,
            phone_number=phone_number,
        ).first()
        if existing:
            return existing

    order = Order(
        email=email,
        phone_number=phone_number,
        customer_note=customer_note,
        basket_id=current_basket_id,
        ip_address=ip_address,
        shipping_address=shipping_address,
        billing_address=billing_address,
        shipping_rate=shipping_rate,
    )
    order.save()

    # Create the order items & compute total
    total = 0
    for item in basket_items:
        total += item.total()
        order_item = OrderItem(
            product=item.variant,
            quantity=item.quantity,
            order=order
        )
        order_item.save()

    order.decrease_stock()
    order.save()

    if capture_payment:
        desc = _("Payment from {email} for order id #{order_id}").format(email=email, order_id=order.id)
        try:
            transaction_id = GATEWAY.create_payment(
                request,
                total + shipping_rate,
                description=desc
            )
            order.payment_date = timezone.now()
            order.transaction_id = transaction_id
            # Once the order has been successfully taken, we can empty the basket
            destroy_basket(request)
        except PaymentError:
            order.status = order.FAILURE

        order.save()

    return order
