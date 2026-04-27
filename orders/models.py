from django.db import models
from books.models import Book
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    email = models.EmailField(_("Email"))
    address = models.CharField(_("Address"), max_length=250)
    postal_code = models.CharField(_("Postal code"), max_length=20)
    city = models.CharField(_("City"), max_length=100)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    paid = models.BooleanField(_("Paid"), default=False)
    stripe_id = models.CharField(_("Stripe ID"), max_length=255, blank=True)
    discount = models.IntegerField(_("Discount"), default=0)

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        related_name="order_items",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
