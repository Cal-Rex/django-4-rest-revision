from django.db import models

# Create your models here.
class Publication(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"publication {self.pk}: {self.title}"
