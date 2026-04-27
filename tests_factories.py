import factory

from books.models import Book, Category
from orders.models import Order, OrderItem


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"Book {n}")
    price = "10.00"
    is_available = True
    category = factory.SubFactory(CategoryFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    first_name = "John"
    last_name = "Doe"
    email = "john@example.com"
    address = "Test street"
    postal_code = "12345"
    city = "Kyiv"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)
    price = "10.00"
    quantity = 2