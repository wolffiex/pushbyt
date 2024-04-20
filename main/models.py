from django.db import models
from django.utils import timezone
import tempfile

class Animation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    file_path = models.FilePathField(path=tempfile.gettempdir())
    start_time = models.DateTimeField()
    served_at = models.DateTimeField(null=True, blank=True, default=None)
