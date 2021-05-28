from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown


class Vibe(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=4000)
    topics = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='vibe_author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    sentiment = models.CharField(null=True, max_length=8)

    def get_vibe_revibes(self):
        return Revibe.objects.filter(original=self).order_by('created_at')

    def get_vibe_count(self):
        return Vibe.objects.filter(created_by=self.created_by).count()

    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))


class Revibe(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=4000)
    original = models.ForeignKey(Vibe, related_name='revibe_original', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='revibe_author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    sentiment = models.CharField(null=True, max_length=8)

    def get_body_as_markdown(self):
        return mark_safe(markdown(self.body, safe_mode='escape'))
