import pytest
from books.models import Book
from orders.models import Order, OrderItem
from tests_factories import BookFactory, OrderFactory, OrderItemFactory


@pytest.mark.django_db
def test_book_creation():
    book = BookFactory()
    assert book.id is not None
    assert book.title.startswith("Book")


@pytest.mark.django_db
def test_book_price():
    book = BookFactory(price="20.00")
    assert str(book.price) == "20.00"


@pytest.mark.django_db
def test_order_creation():
    order = OrderFactory()
    assert order.id is not None
    assert order.email == "john@example.com"


@pytest.mark.django_db
def test_order_item_creation():
    item = OrderItemFactory()
    assert item.id is not None
    assert item.quantity == 2


@pytest.mark.django_db
def test_order_item_relation():
    item = OrderItemFactory()
    assert item.order is not None
    assert item.book is not None


@pytest.mark.django_db
def test_multiple_books():
    books = BookFactory.create_batch(3)
    assert len(books) == 3


@pytest.mark.django_db
def test_order_total_items():
    order = OrderFactory()
    OrderItemFactory.create_batch(5, order=order)
    assert order.items.count() == 5
    