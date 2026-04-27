import pytest
from django.urls import reverse
from tests_factories import BookFactory


@pytest.mark.django_db
def test_books_list_view(client):
    BookFactory()
    response = client.get(reverse("books:list"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail_view(client):
    book = BookFactory()
    response = client.get(reverse("books:detail", args=[book.id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_cart_detail_view(client):
    response = client.get(reverse("cart:cart_detail"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_order_create_view_get(client):
    response = client.get(reverse("orders:order_create"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_async_books_count_view(client):
    BookFactory.create_batch(2)
    response = client.get(reverse("books:async_books_count"))
    assert response.status_code == 200
    assert response.json()["books_count"] >= 2


@pytest.mark.django_db
def test_async_available_books_count_view(client):
    BookFactory.create_batch(3, is_available=True)
    response = client.get(reverse("books:async_available_books_count"))
    assert response.status_code == 200
    assert response.json()["available_books_count"] >= 3


@pytest.mark.django_db
def test_async_first_book_view(client):
    book = BookFactory(title="Async Book")
    response = client.get(reverse("books:async_first_book"))
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Async Book"