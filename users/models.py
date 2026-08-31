from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=50, blank=True)
    password = models.CharField(max_length=120)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)

    @property
    def is_authenticated(self):
        return True