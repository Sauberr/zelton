from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='image')
    phone = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Profile'

    def __str__(self):
        return f"{self.user.username} - {self.full_name} = {self.bio}"
