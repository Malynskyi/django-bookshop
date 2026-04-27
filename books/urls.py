from django.urls import path
from books.views import (
    create_meeting,
    all_meeting,
    MainPage,
    BookListView,
    BookDetail,
    CreateMeeting,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    LibrarianPageView,
    async_books_count,
    async_available_books_count,
    async_first_book,
)
                        
from books.awkward_file import book_list as awkward_all_rec

app_name = 'books' 

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('create-meeting/', create_meeting, name='create_meeting'),
    path('create-meeting-cbv/', CreateMeeting.as_view(), name='create_meeting_cbv'),
    path('all-meetings/', all_meeting, name='all_meeting'),
    path('<int:pk>/', BookDetail.as_view(), name='detail'),
    path('create/', BookCreateView.as_view(), name='create'),
    path('<int:pk>/update/', BookUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='delete'),
    path('librarian-page/', LibrarianPageView.as_view(), name='librarian_page'),
    path("async/books-count/", async_books_count, name="async_books_count"),
    path("async/available-books-count/", async_available_books_count, name="async_available_books_count"),
    path("async/first-book/", async_first_book, name="async_first_book"),
]


