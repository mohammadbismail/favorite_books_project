from django.db import models
import re


class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["firstname"]) < 2:
            errors["firstname"] = "First Name should be minimum 2 characters"
        if len(data["lastname"]) < 2:
            errors["lastname"] = "Last Name should be minimum 2 characters"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        if data["password"] != data["passconf"] and data["passconf"] != 0:
            errors["email"] = "Passwords must match & can't be empty"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # likes_books = list of books that user likes
    # uploaded_books = list of books that user uploads
    objects = UserManager()


class BookManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data["title"]) < 1:
            errors["title"] = "Title can't be empty!"
        if len(data["description"]) < 5:
            errors["description"] = "Description has to be minimum 5 characters"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    #the user who uploaded a certain book
    users_who_like = models.ManyToManyField(User, related_name="likes_books")
    #list of users who like a certain book
    objects = BookManager()
