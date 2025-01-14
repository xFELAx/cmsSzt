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
    label = models.CharField(max_length=20, null=False)
    content = models.TextField()
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
    
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name="services"
    )
    order_number = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    icon = models.CharField(max_length=100000, null=False)
    description = models.TextField()
    
    class Meta:
        db_table = "services"
        ordering = ["order_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["order_number"], name="unique_service_order"
            )
        ]
        
    def __str__(self):
        return f"{self.name}"

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    order_number = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    logo = models.CharField(max_length=100000, null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="brands")
    last_edited_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="edited_brands")
    last_edited_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "brands"
        ordering = ["order_number"]
        constraints = [models.UniqueConstraint(fields=['order_number'], name="unique_brand_order")]

    def __str__(self):
        return self.name

class Work(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    order_number = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    tags = models.CharField(max_length=50)
    description = models.TextField()
    last_edited_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="edited_works")
    last_edited_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "works"
        ordering = ["order_number"]
        constraints = [models.UniqueConstraint(fields=['order_number'], name="unique_work_order")]

    def __str__(self):
        return self.name

class BrandWork(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    class Meta:
        db_table = "brands_works"
        constraints = [models.UniqueConstraint(fields=['brand', 'work'], name='unique_brand_work')]

    def __str__(self):
        return self.brand.name + " " + self.work.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    order_number = models.SmallIntegerField(null=False)
    author_name = models.CharField(max_length=30)
    author_surname = models.CharField(max_length=60)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    last_edited_by = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="edited_reviews")
    last_edited_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        constraints = [models.UniqueConstraint(fields=['order_number'], name="unique_review_order")]

    def __str__(self):
        return self.content
