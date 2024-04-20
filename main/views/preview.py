from django.utils import timezone
from django.shortcuts import redirect
from django.templatetags.static import static
from main.models import Animation

def get_preview(request):
    now = timezone.now()
    anim = Animation.get_next_animation(now)
    if anim:
        anim.served_at = now
        anim.save()
        return redirect(f"/pushbyt/{anim.file_path}")
    return redirect(static("error.webp"))
