from django.db import models
from django.conf import settings
from search.models import Song

class DownloadedSong(models.Model):
    """Model definition for DownloadedSong."""

    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    path = models.FilePathField(path=settings.MEDIA_DIR, blank=True)
    download_count = models.PositiveIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for DownloadedSong."""

        verbose_name = 'DownloadedSong'
        verbose_name_plural = 'DownloadedSongs'

    def __str__(self):
        """Unicode representation of DownloadedSong."""
        return str(self.song)
