from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    author_pseudonym = models.CharField(max_length=64, null=True, blank=True, unique=True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.author_pseudonym if self.author_pseudonym else self.username


class Book(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1500, null=True, blank=True)
    auther = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='cover_images', null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.auther}'
