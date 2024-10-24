from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='cover_images/')  # Requires Pillow library for handling images

    def __str__(self):
        return self.title
    
class Book(models.Model):
    title = models.CharField(max_length=255)  # Tytuł książki
    author = models.CharField(max_length=255)  # Autor książki
    cover_image = models.ImageField(upload_to='', null=True, blank=True)  # Zdjęcie okładki
    isbn = models.CharField(max_length=13, unique=True)  # Numer ISBN

    def __str__(self):
        return f"{self.title} by {self.author}"
    
class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Powiązanie z użytkownikiem
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Powiązanie z książką
    is_for_sale = models.BooleanField(default=False)  # Czy książka jest na sprzedaż
    condition = models.CharField(max_length=50)  # Stan książki (np. 'nowa', 'używana', 'zniszczona')
    front_image = models.ImageField(upload_to='user_books/front_images/', null=True, blank=True)  # Zdjęcie przednie
    back_image = models.ImageField(upload_to='user_books/back_images/', null=True, blank=True)  # Zdjęcie tylne
    created_at = models.DateTimeField(auto_now_add=True)  # Pole do przechowywania daty dodania rekordu

    def __str__(self):
        return f"{self.user.username} owns {self.book.title}"
