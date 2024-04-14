from django.http import Http404, HttpResponse
from django.shortcuts import render
from main.animation.rays import clock_rays
from io import BytesIO
import logging
import base64

logger = logging.getLogger(__name__)


def get_webp(request, name: str):
    logger.info(f"Anim {name}")
    frames = None
    if name == "rays":
        frames = clock_rays()

    if frames:
        output = BytesIO()
        # Save the image to the response
        frames[0].save(
            output,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=100,
            loop=0,
            quality=100,
        )
        response = HttpResponse(content_type="image/webp")
        response.write(output.getvalue())

        return response

    raise Http404(f"Unknown animation {name}")


def get_player(request, name: str):
    frames = None
    if name == "rays":
        frames = clock_rays()
        frame_bytes = (encode_frame(frame) for frame in frames)
        return render(
            request,
            "player.html",
            {"frames": frame_bytes, "title": name, "frame_count": len(frames)},
        )

    raise Http404(f"Unknown animation {name}")


def encode_frame(frame):
    output = BytesIO()
    frame.save(
        output,
        format="WEBP",
        quality=100,
    )
    return base64.b64encode(output.getvalue()).decode("utf-8")
