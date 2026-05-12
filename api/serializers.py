from rest_framework import serializers

from books.models import Book, Category
from orders.models import Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "books_count"]


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "price",
            "description",
            "published_at",
            "is_available",
            "category",
            "category_id",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
        write_only=True,
    )

    class Meta:
        model = OrderItem
        fields = ["id", "book", "book_id", "price", "quantity", "get_cost"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
            "created",
            "updated",
            "paid",
            "stripe_id",
            "discount",
            "items",
            "total_cost",
        ]
        read_only_fields = ["paid", "stripe_id", "created", "updated"]

    def get_total_cost(self, obj):
        return obj.get_total_cost()


class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, max_value=20)
    override = serializers.BooleanField(default=False)