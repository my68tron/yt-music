from django.db import models

class Song(models.Model):
    song_name = models.CharField(max_length=264, unique=True)
    song_url = models.URLField(unique=True, blank=True)
    song_path = models.FilePathField(unique=True, blank=True)

    def __str__(self):
        return self.song_name
    
class Search(models.Model):
    search_title = models.CharField(max_length=264, unique=True)
    
    def __str__(self):
        return self.search_title