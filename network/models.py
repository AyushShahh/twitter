from django.contrib.auth.models import AbstractUser
from django.db import models


# symetrical
class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')
    likes = models.ManyToManyField('Post', blank=True, related_name='liked_by')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}: {self.text[:50]}{'...' if len(self.text) > 50 else ''}"
    