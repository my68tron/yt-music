from django.db import models
from django.conf import settings

class Song(models.Model):
    name = models.CharField(max_length=264, unique=True)
    duration = models.CharField(max_length=264)
    url = models.URLField(unique=True)
    img_url = models.URLField(unique=True)
    channel_name = models.CharField(max_length=264)
    channel_url = models.URLField()
    path = models.FilePathField(path=settings.MEDIA_DIR)
    uploaded = models.CharField(max_length=264)
    views = models.CharField(max_length=264)
    download_count = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Search(models.Model):
    title = models.CharField(max_length=264, unique=True)
    songs = models.CharField(max_length=264)
    
    def __str__(self):
        return self.title