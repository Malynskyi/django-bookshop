import stripe 
from django.conf import settings 
from django.urls import reverse 
from django.shortcuts import render, redirect
from django.db import transaction

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY


@transaction.atomic
def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            request.session["order_id"] = order.id

            send_mail(
                'Order created',
                f'Your order {order.id} has been created successfully.',
                'admin@example.com',
                [order.email],
                fail_silently=True,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    book=item["book"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            cart.clear()
            return redirect("orders:payment_process")

    else:
        form = OrderCreateForm()

    return render(request, "orders/create.html", {"cart": cart, "form": form})

def payment_process(request):
    order_id = request.session.get("order_id")
    if not order_id:
         return redirect("orders:order_create")

    order = Order.objects.get(id=order_id)
    order_items = order.items.all()

    if not order_items.exists():
        return render(request, "orders/cancel.html", {"message": "Order has no items."})

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.book.title,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": item.quantity,
            }
            for item in order_items 
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("orders:payment_success")),
        cancel_url=request.build_absolute_uri(reverse("orders:payment_cancel")),
    )

    return redirect(session.url)

def payment_success(request):
    order_id = request.session.get("order_id")

    if order_id:
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()

    return render(request, "orders/success.html")

def payment_cancel(request):
    return render(request, "orders/cancel.html")