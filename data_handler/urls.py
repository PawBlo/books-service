from django.urls import path
from .views import *

urlpatterns = [
   path("entries/list/", list_entries, name="list-entries"),
   path("entries/add_book_to_user/",add_book_to_user, name = "add-book-to-user"),
   path("entries/add_book/", add_book, name = "add-book"),
   path("entries/get_user_books/", get_user_books, name = "get-user-books"),
   path('entries/get_all_books/', get_all_books, name = "get-all-books"),
   path('entries/get_book/', get_book, name = "get-book"),
   path('entries/search_users_with_book/', search_users_with_book, name = "search_users_with_book"),
   path('entries/get_latest_books/', get_latest_books, name = 'get-latest-books'),
]