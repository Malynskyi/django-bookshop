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

from typing import Any 

from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from django.db.models import Q, Count
from books.forms import MeetingForm
from .models import Book, Category, Meeting
from books.mixins import (
    AuthorFilteringMixin,
    AuthorFilteredTemplateResponseMixin,
    BookNameFilterMixin,
    AuthorNameFilterMixin,
    AuthorBookNameMixin,
    GodModRequiredMixin
)
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy


class MainPage(GodModRequiredMixin, AuthorFilteredTemplateResponseMixin, TemplateView):
    template_name = 'books/index.html'
    context_param_name = 'recent'
    model = Book


class BookCreateView(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'description', 'category', 'is_available']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:list')
    permission_required = 'books.add_book'

class BookListView(ListView):
    model = Book
    template_name = 'books/all_records.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.GET.get('title')
        author = self.request.GET.get('author')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__username__icontains=author)

        return queryset
    

class BookDetail(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/details.html'
    context_object_name = 'book'
    queryset = Book.objects.filter(is_available=True)


def category_list(request):
    categories = Category.objects.annotate(book_count=Count('books'))

    return render(request, 'books/categories.html', {
        'categories': categories
    })


def all_meeting(request):
    all_meets = Meeting.objects.all()
    return render(request, 'all_meets.html', {'meets': all_meets})

def create_meeting(request):
    form = MeetingForm()
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_meeting')
    return render(request, 'create_meeting.html', {'form': form})


class CreateMeeting(FormView):
    template_name = 'create_meeting.html'
    form_class = MeetingForm
    success_url = reverse_lazy('books:list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

class BookUpdateView(PermissionRequiredMixin, UpdateView): 
    model = Book
    fields = ['title', 'description', 'category', 'is_available']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('books:list')
    permission_required = 'books.change_book'


class BookDeleteView(PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:list')
    permission_required = 'books.delete_book'


class LibrarianPageView(PermissionRequiredMixin, TemplateView):
    template_name = "books/librarian_page.html"
    permission_required = "books.add_book"



