from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User
from profiles.models import Profile


# Create your models here.
class Follower(models.Model):
    owner = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at',]
        constraints = [UniqueConstraint(fields=['owner', 'followed'], name='unique_follow')]

    def __str__(self):
        return f"{self.owner} following {self.followed}"