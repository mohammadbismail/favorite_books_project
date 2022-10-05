from django.shortcuts import render, redirect
from .models import User, Book
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, "registration.html")


def add_user(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")

    password_plain = request.POST["password"]
    password_hash = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()

    User.objects.create(
        first_name=request.POST["firstname"],
        last_name=request.POST["lastname"],
        email=request.POST["email"],
        password=password_hash,
    )
    return redirect("/")


def login_user(request):
    user = User.objects.filter(email=request.POST["email"])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(
            request.POST["password"].encode(), logged_user.password.encode()
        ):
            request.session["userid"] = logged_user.id
            request.session["firstname"] = logged_user.first_name
            request.session["lastname"] = logged_user.last_name
            return redirect("/books")
        return redirect("/")


def all_books_page(request):
    if "userid" not in request.session:
        return redirect("/")
    context = {
        # all books
        "books": Book.objects.all(),
        # query of books(Childs) for one parent(User) (One --> Many)
        "books_list_uploaded_by_user": User.objects.get(id=request.session["userid"]).books_uploaded.all(),
        "books_list_liked_by_user": User.objects.get(
            id=request.session["userid"]
        ).likes_books.all(),
    }
    return render(request, "all_books.html", context)


def logout_user(request):
    del request.session["userid"]
    del request.session["firstname"]
    del request.session["lastname"]
    return redirect("/")


def add_book(request):
    errors = Book.objects.validator(request.POST)
    print("hello")
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/books/")
    Book.objects.create(
        title=request.POST["title"],
        description=request.POST["description"],
        uploaded_by=User.objects.get(id=request.session["userid"]),
    )
    return redirect("/books/")


def show_book(request, book_id):
    context = {
        "book": Book.objects.get(id=book_id),
        # query of list of users who like this book
        "user_list_who_like_this_book": Book.objects.get(
            id=book_id
        ).users_who_like.all(),
        # query of books(Childs) for one parent(User) (One --> Many)
        "books_list_uploaded_by_user": User.objects.get(
            id=request.session["userid"]
        ).books_uploaded.all(),
        "book_list_liked_by_user": User.objects.get(id=request.session["userid"]).likes_books.all(),
    }
    print(context["user_list_who_like_this_book"])
    print(context["books_list_uploaded_by_user"])
    return render(request, "single_book.html", context)


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect(f"/books/")


def update_book(request):
    # id of book need to be updated coming from hidden input
    book = Book.objects.get(id=request.POST["bookid"])
    book.title = request.POST["title"]
    book.description = request.POST["description"]
    book.save()
    return redirect("/books/")


def add_book_to_user_list_of_favorites(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session["userid"])
    this_book.users_who_like.add(this_user)
    return redirect("/books")


def remove_book_from_user_favorite_list(request, book_id):
    this_book = Book.objects.get(id=book_id)
    this_user = User.objects.get(id=request.session["userid"])
    this_book.users_who_like.remove(this_user)
    return redirect("/books")
