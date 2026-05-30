import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from tests_factories import BookFactory
from books.models import Category
from orders.models import Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username="dmytro",
        email="malynskyidmytro@gmail.com",
        password="testpass123",
    )


@pytest.fixture
def admin_user():
    User = get_user_model()
    return User.objects.create_superuser(
        username="bro",
        email="bro@myboy.com",
        password="bropass423",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.mark.django_db
def test_api_books_list(api_client):
    BookFactory.create_batch(2)
    response = api_client.get("/api/books/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_books_pagination(api_client):
    BookFactory.create_batch(25)
    response = api_client.get("/api/books/")
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 20


@pytest.mark.django_db
def test_api_books_detail(api_client):
    book = BookFactory()
    response = api_client.get(f"/api/books/{book.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_books_search(api_client):
    BookFactory(title="Django API Book")
    response = api_client.get("/api/books/?search=Django")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_books_ordering(api_client):
    BookFactory.create_batch(3)
    response = api_client.get("/api/books/?ordering=price")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_books_filter_available(api_client):
    BookFactory(is_available=True)
    response = api_client.get("/api/books/?is_available=True")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_book_create_requires_auth(api_client):
    response = api_client.post("/api/books/", {"title": "New Book", "price": "10.00"})
    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_api_book_create_authenticated(auth_client):
    response = auth_client.post(
        "/api/books/",
        {"title": "New Book", "price": "10.00", "is_available": True},
    )
    assert response.status_code in [201, 400]


@pytest.mark.django_db
def test_api_categories_list(api_client):
    Category.objects.create(name="Programming", slug="programming")
    response = api_client.get("/api/categories/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_categories_detail(api_client):
    category = Category.objects.create(name="Python", slug="python")
    response = api_client.get(f"/api/categories/{category.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_categories_search(api_client):
    Category.objects.create(name="Backend", slug="backend")
    response = api_client.get("/api/categories/?search=Backend")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_category_create_requires_auth(api_client):
    response = api_client.post("/api/categories/", {"name": "New", "slug": "new"})
    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_api_order_list_requires_auth(api_client):
    response = api_client.get("/api/orders/")
    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_api_order_list_authenticated(auth_client, user):
    Order.objects.create(
        first_name="Dmytro",
        last_name="Malynskyi",
        email=user.email,
        address="Olen street",
        postal_code="68341",
        city="Odessa",
    )
    response = auth_client.get("/api/orders/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_order_detail_authenticated(auth_client, user):
    order = Order.objects.create(
        first_name="Dmytro",
        last_name="Malynskyi",
        email=user.email,
        address="Baran street",
        postal_code="67676",
        city="Odessa",
    )
    response = auth_client.get(f"/api/orders/{order.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_admin_can_see_orders(admin_client):
    Order.objects.create(
        first_name="Dmytro",
        last_name="Malynskyi",
        email="malynskyidmytro@gmail.com",
        address="Loch street",
        postal_code="67676",
        city="Odessa",
    )
    response = admin_client.get("/api/orders/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_order_filter_paid(auth_client, user):
    Order.objects.create(
        first_name="Dmytro",
        last_name="Malynskyi",
        email=user.email,
        address="Dmytro street",
        postal_code="66766",
        city="Odessa",
        paid=True,
    )
    response = auth_client.get("/api/orders/?paid=True")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_cart_requires_auth(api_client):
    response = api_client.get("/api/cart/")
    assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_api_cart_list_authenticated(auth_client):
    response = auth_client.get("/api/cart/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_cart_add_book(auth_client):
    book = BookFactory(price="25.00")
    response = auth_client.post(
        "/api/cart/add/",
        {"book_id": book.id, "quantity": 2, "override": False},
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_api_cart_remove_book(auth_client):
    book = BookFactory(price="25.00")
    auth_client.post(
        "/api/cart/add/",
        {"book_id": book.id, "quantity": 1, "override": False},
        format="json",
    )
    response = auth_client.post(
        "/api/cart/remove/", {"book_id": book.id}, format="json"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_cart_clear(auth_client):
    book = BookFactory(price="25.00")
    auth_client.post(
        "/api/cart/add/",
        {"book_id": book.id, "quantity": 1, "override": False},
        format="json",
    )
    response = auth_client.post("/api/cart/clear/", {}, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_jwt_token_obtain(api_client, user):
    response = api_client.post(
        "/api/token/",
        {"username": "dmytro", "password": "testpass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_api_jwt_token_refresh(api_client, user):
    obtain = api_client.post(
        "/api/token/",
        {"username": "dmytro", "password": "testpass123"},
        format="json",
    )
    refresh = obtain.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/",
        {"refresh": refresh},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_api_jwt_token_verify(api_client, user):
    obtain = api_client.post(
        "/api/token/",
        {"username": "dmytro", "password": "testpass123"},
        format="json",
    )
    access = obtain.data["access"]

    response = api_client.post(
        "/api/token/verify/",
        {"token": access},
        format="json",
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_docs_available(api_client):
    response = api_client.get("/api/docs/")
    assert response.status_code == 200
