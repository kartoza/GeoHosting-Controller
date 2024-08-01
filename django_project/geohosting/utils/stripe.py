"""Utility functions for working with stripe."""
import stripe
from django.conf import settings

from geohosting.models.product import Package
from geohosting.models.sales_order import SalesOrder, SalesOrderStatus

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_price_id(package: Package):
    """Create package price on stripe."""

    if package.price and not package.stripe_price_id:
        obj = stripe.Price.create(
            currency=package.currency,
            unit_amount=1000,
            recurring={
                "interval": package.periodicity.replace('ly', '')
            },
            product_data={
                "name": package.name
            },
        )
        package.stripe_price_id = obj.id
        package.save()


def get_price_id(package: Package):
    """Create package price on stripe."""
    if not package.stripe_price_id:
        create_price_id(package)

    return package.stripe_price_id


def get_checkout_status(order: SalesOrder):
    """Get checkout status."""
    detail = stripe.checkout.Session.retrieve(order.stripe_checkout_id)
    if detail.invoice:
        order.order_status = SalesOrderStatus.PAID
        order.save()
    return None
