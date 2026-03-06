# from django.shortcuts import render
# from books.models import Book
# from demo_app.models import DemoModel


# def all_records(request):
#     books = Book.objects.all()
#     demo_models = DemoModel.objects.filter(is_visible=True)
#     return render(
#         request,
#         'all_records.html',
#         {'books': books, 'demo_models': demo_models}
#     )


from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Book, Category


def book_list(request):
    books = Book.objects.all()

    search = request.GET.get('q')

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    return render(request, 'books/book_list.html', {
        'books': books
    })


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    return render(request, 'books/book_detail.html', {
        'book': book
    })


def category_list(request):
    categories = Category.objects.annotate(book_count=Count('books'))

    return render(request, 'books/categories.html', {
        'categories': categories
    })
