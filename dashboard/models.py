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


class SocialMedia(models.Model):
    id = models.AutoField(primary_key=True)
    icon = models.CharField(max_length=100000)
    link = models.URLField(max_length=100)
    last_edited_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="edited_socials"
    )
    last_edited_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    order_number = models.SmallIntegerField(null=False, unique=True)

    class Meta:
        ordering = ["order_number"]
        db_table = "social_medias"
        constraints = [
            models.UniqueConstraint(fields=["id"], name="AK_7"),
            models.UniqueConstraint(
                fields=["order_number"], name="unique_order_number"
            ),
        ]

class Section(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=False)
    order_number = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    label = models.CharField(max_length=10, null=False)
    content = models.TextField(null=True, blank=True)
    last_edited_by = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="edited_sections"
    )
    last_edited_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "sections"
        ordering = ["order_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["order_number"], name="unique_section_order"
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.label})"


class TextLine(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=255, null=False)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="text_lines"
    )

    class Meta:
        db_table = "text_lines"

    def __str__(self):
        return f"Text line for section: {self.section.name}"