from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse


class Animation(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    file_path = models.FilePathField(path="render")
    start_time = models.DateTimeField()
    served_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        indexes = [models.Index(fields=["start_time"])]

    def clean(self):
        super().clean()
        if self.start_time.microsecond != 0:
            raise ValidationError("Start time milliseconds must be zero.")
        if self.start_time.second not in [0, 15, 30, 45]:
            raise ValidationError("Start time seconds must be one of 0, 15, 30, or 45.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the model before saving
        super().save(*args, **kwargs)

    @classmethod
    def get_next_animation(cls, current_time:datetime):
        return (
            cls.objects.filter(start_time__gt=current_time)
            .order_by("start_time")
            .first()
        )

class Lock(models.Model):
    name = models.CharField(max_length=100, unique=True)
    acquired = models.BooleanField(default=False)
