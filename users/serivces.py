import stripe
from django.conf import settings

from users.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def create_product(prod: Payment):
    """
    Создает новый продукт в Stripe
    """

    product = prod.paid_lesson if prod.paid_lesson else prod.paid_course
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.get('id')


def create_price(prod: Payment, stripe_prod):
    """
    Создает цену в Stripe
    """
    product_price = prod.amount

    return stripe.Price.create(
        currency="rub",
        unit_amount=product_price * 100,
        product_data={"name": stripe_prod}
    )


def create_session(price):
    """
    Создает сессию в Stripe для оплаты
    """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success_pay/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
