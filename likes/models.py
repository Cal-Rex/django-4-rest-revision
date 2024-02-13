from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment

# Create your models here.
class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [UniqueConstraint(fields=['owner', 'post'], name='unique_like')]

    def __str__(self):
        return f"{self.owner}'s post on {self.post}"
