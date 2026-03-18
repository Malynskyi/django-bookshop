from django.shortcuts import render
from django.db.models import Q 
from .models import Book 
from django.views.generic import View
from django.http import HttpResponse 


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


class BookOrDemoView(View):
    model = ...
    def get_queryset(self):
        qs = self.model.objects.all()
        return qs
    
    def get(self, request):
        context_obj = self.get_queryset()
        return render(
            request, 
            'books/all_records.html', 
            {'books': context_obj}
        )