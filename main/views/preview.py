from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.templatetags.static import static

def get_preview(request):
    showtime = datetime.now() + timedelta(seconds=5)
    hour = showtime.hour
    minute = showtime.minute
    part = showtime.second // 15
    anim_file = f"anim-{hour:02d}-{minute:02d}-{part}.webp"
    return redirect(static(str(anim_file)))
