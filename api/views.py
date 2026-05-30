from django.shortcuts import render
from django.db.models import Count
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from books.models import Book, Category
from cart.cart import Cart
from orders.models import Order

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    BookSerializer,
    CartItemSerializer,
    CategorySerializer,
    OrderSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(books_count=Count("books"))
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ["slug", "name"]
    search_fields = ["name", "slug"]
    ordering_fields = ["id", "name"]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("category", "author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["category", "is_available", "price"]
    search_fields = ["title", "description"]
    ordering_fields = ["id", "title", "price", "published_at"]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    filterset_fields = ["paid", "email", "city"]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["id", "created", "updated"]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items__book").all()

        if self.request.user.is_staff:
            return queryset

        return queryset.filter(email=self.request.user.email)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = Cart(request)
        data = []

        for item in cart:
            data.append(
                {
                    "book": BookSerializer(item["book"]).data,
                    "quantity": item["quantity"],
                    "price": str(item["price"]),
                    "total_price": str(item["total_price"]),
                }
            )

        return Response(
            {
                "items": data,
                "total_price": str(cart.get_total_price()),
            }
        )

    @action(detail=False, methods=["post"])
    def add(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = get_object_or_404(Book, id=serializer.validated_data["book_id"])
        cart = Cart(request)
        cart.add(
            book=book,
            quantity=serializer.validated_data["quantity"],
            override_quantity=serializer.validated_data["override"],
        )

        return Response(
            {"detail": "Book added to cart"}, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"])
    def remove(self, request):
        book_id = request.data.get("book_id")
        book = get_object_or_404(Book, id=book_id)

        cart = Cart(request)
        cart.remove(book)

        return Response({"detail": "Book removed from cart"})

    @action(detail=False, methods=["post"])
    def clear(self, request):
        cart = Cart(request)
        cart.clear()

        return Response({"detail": "Cart cleared"})
