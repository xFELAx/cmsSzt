from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If this video is being set to active, deactivate all other videos
        if self.is_active:
            Video.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title