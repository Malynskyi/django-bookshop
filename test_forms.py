# Generated with AI, reviewed and modified
import pytest

from cart.forms import CartAddBookForm
from orders.forms import OrderCreateForm


def test_cart_add_book_form_valid():
    form = CartAddBookForm(data={"quantity": 1, "override": False})
    assert form.is_valid()


def test_cart_add_book_form_invalid_quantity():
    form = CartAddBookForm(data={"quantity": 1000, "override": False})
    assert not form.is_valid()


def test_cart_add_book_form_has_quantity_field():
    form = CartAddBookForm()
    assert "quantity" in form.fields


def test_order_create_form_valid():
    form = OrderCreateForm(data={
        "first_name": "Dmytro",
        "last_name": "Mal",
        "email": "malynskyidmytro@gmail.com",
        "address": "Zelensky street",
        "postal_code": "12345",
        "city": "Odessa",
    })
    assert form.is_valid()


def test_order_create_form_invalid_email():
    form = OrderCreateForm(data={
        "first_name": "Dmytro",
        "last_name": "Malynskyi",
        "email": "not-an-email",
        "address": "Zelensky street",
        "postal_code": "12345",
        "city": "Odessa",
    })
    assert not form.is_valid()