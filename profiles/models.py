from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """model for the profile table"""
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """signal to create a profile entry 
    whenever a new user is added to the User table"""
    # Because we are passing this function 
    # to the post_save.connect method
    # it requires the following arguments:
    # 1. the sender model,
    # 2. its instance
    # 3. created  - which is a boolean value of 
    #    whether or not the instance has just been created
    # 4. and kwargs.
    if created:
        # if created is True, we’ll create a profile  
        # whose owner is going to be that user.
        Profile.objects.create(owner=instance)
        
# not part of the function, but this would be sitting
# directly under it
post_save.connect(create_profile, sender=User)