from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    books_view_hide_completed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='media/', default="defaultProfilePic.jpg", null=True, blank=True)
    def __str__(self):
        return self.user.username



class BookGenre(models.Model):
    genre = models.CharField(max_length=128)
    def __str__(self):
        return self.genre


class Book(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(BookGenre, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    length = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    def __str__(self):
        return self.title



class Review(models.Model):
    description = models.CharField(max_length=10000)
    stars =  models.PositiveIntegerField(validators=[MaxValueValidator(5),])
    recommendation =  models.BooleanField(default=True)
    readability =  models.PositiveIntegerField(validators=[MaxValueValidator(5),])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book)
    def __str__(self):
        return self.description
