from rest_framework import serializers
from .models import Entry, Book, UserBook
from django.contrib.auth.models import User

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'title', 'cover_image']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'cover_image', 'isbn']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserBookSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested serializer to include user details
    book = BookSerializer(read_only=True)  # Nested serializer to include book details

    class Meta:
        model = UserBook
        fields = ['id', 'user', 'book', 'is_for_sale', 'condition', 'front_image', 'back_image']