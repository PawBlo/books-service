from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='cover_images/')  # Requires Pillow library for handling images

    def __str__(self):
        return self.title