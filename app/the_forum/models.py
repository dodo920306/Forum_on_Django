from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(blank=True)
    login_count = models.PositiveIntegerField(default=0)
    post_count = models.PositiveIntegerField(default=0)

    def increase_login_count(self):
        self.login_count += 1
        self.save()


class Board(models.Model):
    name = models.CharField()
    moderators = models.ManyToManyField(User, related_name='moderated_boards')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
