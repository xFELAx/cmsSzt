from django.db import models
from django.utils import timezone


class Video(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=False)
    url = models.URLField(max_length=100)
    last_edited_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="edited_videos"
    )
    last_edited_date = models.DateTimeField(auto_now=True)  # Changed to auto_now

    class Meta:
        db_table = "videos"
        constraints = [models.UniqueConstraint(fields=["id"], name="AK_6")]

    def save(self, *args, **kwargs):
        if self.is_active:
            Video.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Video {self.id} - {self.url}"
