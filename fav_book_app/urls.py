from django.urls import path
from . import views

urlpatterns = [
    #route shared between several pages
    path("logout_user/", views.logout_user),
    # start of registration page routes
    path("", views.index),
    path("add_user/", views.add_user),
    path("login_user/", views.login_user),
    #end
    #start of all books page routes 
    path("books/", views.all_books_page),
    path("add_book/", views.add_book),
    path("books/<int:book_id>/", views.show_book),
    path("books/add_book_to_user_list_of_favorites/<int:book_id>/",views.add_book_to_user_list_of_favorites),
    #end
    #start of specific book details routes
    path("update_book/",views.update_book), 
    path("delete_book/<int:book_id>/",views.delete_book),
    path("books/remove_book_from_user_favorite_list/<int:book_id>/",views.remove_book_from_user_favorite_list),
]
