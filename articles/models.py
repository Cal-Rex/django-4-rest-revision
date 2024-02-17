from django.db import models
from publications.models import Publication

# Create your models here.
class Article(models.Model):
    headline = models.CharField(max_length=250)
    publications = models.ManyToManyField(Publication)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.headline}"
