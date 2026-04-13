from django.shortcuts import get_object_or_404, redirect, render
from books.models import Book
from .cart import Cart
from .forms import CartAddBookForm


def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)

    if form.is_valid():
        cart.add(
            book=book,
            quantity=form.cleaned_data["quantity"],
            override_quantity=form.cleaned_data["override"]
        )

    return redirect("cart:cart_detail")


def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item["update_quantity_form"] = CartAddBookForm(
            initial={
                "quantity": item["quantity"],
                "override": True
            }
        )

    return render(request, "cart/detail.html", {"cart": cart})