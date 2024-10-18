from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title