from django.utils import timezone
from django.shortcuts import redirect
from django.templatetags.static import static
from main.models import Animation
import logging

logger = logging.getLogger(__name__)
def get_preview(_):
    now = timezone.now()
    anim = Animation.get_next_animation(now)
    if anim:
        if anim.served_at:
            logger.error(f"Already served {anim.file_path} at {anim.served_at} now {now}")
        anim.served_at = now
        anim.save()
        return redirect(f"/pushbyt/{anim.file_path}")
    return redirect(static("error.webp"))
