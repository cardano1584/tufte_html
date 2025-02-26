from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class TransformationContent(models.Model):
    title = models.CharField(max_length=200, unique=True)
    summary = models.CharField(max_length=500)
    description = models.TextField()
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transformation_creator')
    last_modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='transformation_mod_by')
    last_modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class TransformationPostViewTracking(models.Model):
    post = models.ForeignKey(TransformationContent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} viewed {self.post.title} on {self.viewed_at}"

class TransformationPostVersion(models.Model):
    post = models.ForeignKey(TransformationContent, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=500)
    description = models.TextField()
    content = models.TextField()
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    version_created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Version of {self.post.title} by {self.changed_by} on {self.version_created_at}"
