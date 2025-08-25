from django.db import models

# Create your models here.

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="movie/images/", default="movie/images/default.png")
    genre = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
