import pytest
from unittest.mock import patch, Mock
from django.urls import reverse

from tests_factories import BookFactory, OrderFactory, OrderItemFactory
from orders.models import Order


@pytest.mark.django_db
def test_integration_books_page_opens(client):
    BookFactory()
    response = client.get(reverse("books:list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_integration_add_book_to_cart_redirects(client):
    book = BookFactory(price="50.00")
    response = client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 1, "override": False},
    )
    assert response.status_code == 302


@pytest.mark.django_db
def test_integration_cart_contains_added_book(client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 2, "override": False},
    )
    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200
    assert book.title.encode() in response.content


@pytest.mark.django_db
def test_integration_cart_update_quantity(client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 1, "override": False},
    )
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 4, "override": True},
    )
    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_integration_cart_remove_book(client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 1, "override": False},
    )
    response = client.get(reverse("cart:cart_remove", args=[book.id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_integration_order_create_page_opens(client):
    response = client.get(reverse("orders:order_create"))
    assert response.status_code == 302


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_integration_order_create_sends_email(mock_send_mail, client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 1, "override": False},
    )

    response = client.post(reverse("orders:order_create"), {
        "first_name": "Dmytro",
        "last_name": "Malynskyi",
        "email": "malynskyidmytro@gmail.com",
        "address": "Dmytro street",
        "postal_code": "12345",
        "city": "Odessa",
    })

    assert response.status_code == 302
    assert mock_send_mail.called


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_integration_order_created_in_db(mock_send_mail, client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 2, "override": False},
    )

    client.post(reverse("orders:order_create"), {
        "first_name": "Dmytro",
        "last_name": "Malynskyi",
        "email": "malynskyidmytro@gmail.com",
        "address": "Mal street",
        "postal_code": "12345",
        "city": "Odessa",
    })

    assert Order.objects.count() == 1


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_integration_order_items_created(mock_send_mail, client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 3, "override": False},
    )

    order_response = client.post(reverse("orders:order_create"), {
        "first_name": "Dmytro",
        "last_name": "Malynskyi",
        "email": "malynskyidmytro@gmail.com",
        "address": "Dmytro street",
        "postal_code": "12345",
        "city": "Odessa",
    })

    order = Order.objects.first()
    assert order.items.count() == 1


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_integration_order_create_redirects_to_payment(mock_send_mail, client):
    book = BookFactory(price="50.00")
    client.post(
        reverse("cart:cart_add", args=[book.id]),
        {"quantity": 1, "override": False},
    )

    response = client.post(reverse("orders:order_create"), {
        "first_name": "Dmytro",
        "last_name": "Malynskyi",
        "email": "malynskyidmytro@gmail.com",
        "address": "Test street",
        "postal_code": "12345",
        "city": "Odessa",
    })

    assert response.status_code == 302


@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.create")
def test_integration_stripe_checkout_is_called(mock_stripe_create, client):
    order = OrderFactory()
    OrderItemFactory(order=order, price="50.00", quantity=2)

    session = client.session
    session["order_id"] = order.id
    session.save()

    mock_stripe_create.return_value = Mock(url="https://stripe.test/checkout")

    response = client.get(reverse("orders:payment_process"))

    assert response.status_code == 302
    assert mock_stripe_create.called


@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.create")
def test_integration_payment_redirects_to_stripe(mock_stripe_create, client):
    order = OrderFactory()
    OrderItemFactory(order=order, price="50.00", quantity=1)

    session = client.session
    session["order_id"] = order.id
    session.save()

    mock_stripe_create.return_value = Mock(url="https://stripe.test/checkout")

    response = client.get(reverse("orders:payment_process"))

    assert response.url == "https://stripe.test/checkout"


@pytest.mark.django_db
def test_integration_payment_success_marks_order_paid(client):
    order = OrderFactory(paid=False)

    session = client.session
    session["order_id"] = order.id
    session.save()

    response = client.get(reverse("orders:payment_success"))

    order.refresh_from_db()
    assert response.status_code == 200
    assert order.paid is True


@pytest.mark.django_db
def test_integration_payment_cancel_page(client):
    response = client.get(reverse("orders:payment_cancel"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_integration_async_books_count_flow(client):
    BookFactory.create_batch(3)

    response = client.get(reverse("books:async_books_count"))

    assert response.status_code == 200
    assert response.json()["books_count"] >= 3