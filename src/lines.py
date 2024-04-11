from PIL import Image, ImageDraw
import math
import os
from dataclasses import dataclass

width, height = 64, 32
frames = []
duration = 100  # ms per frame (10fps)


image = Image.new("RGB", (width, height), color="black")
frames = [Image.new("RGB", (width, height), color="black")]


def find_intersection(angle):
    center_x = width / 2
    center_y = height / 2

    tan_angle = math.tan(angle)

    if angle < math.pi / 2:
        x = width
        y = center_y + (x - center_x) * tan_angle
    elif angle < math.pi:
        y = height
        x = center_x + (y - center_y) / tan_angle
    elif angle < 3 * math.pi / 2:
        x = 0
        y = center_y - (center_x - x) * tan_angle
    else:
        y = 0
        x = center_x - (center_y - y) / tan_angle

    return x, y


@dataclass
class Point:
    x: float
    y: float

    def to_tuple(self):
        return self.x, self.y


STEPS = 100
SCALE_FACTOR = 4
center = Point(SCALE_FACTOR * (width - 1) / 2, SCALE_FACTOR * (height - 1) / 2)
for step in range(STEPS):
    angle = 2 * math.pi * step / 100
    image = Image.new("RGB", (SCALE_FACTOR * width, SCALE_FACTOR * height), color="black")
    draw = ImageDraw.Draw(image)

    length = 100 * SCALE_FACTOR  # somewhat arbirary chosen to extend beyond boundary
    end = Point(
        center.x + length * math.cos(angle), center.y + length * math.sin(angle)
    )

    draw.line([center.to_tuple(), end.to_tuple()], fill="white", width=SCALE_FACTOR)

    # Downsample the high-resolution image to the desired size
    image_lo = image.resize((width, height), resample=Image.LANCZOS)

    frames.append(image_lo)

os.makedirs("dist", exist_ok=True)
frames[0].save(
    "dist/animation.webp",
    save_all=True,
    append_images=frames[1:],
    duration=duration,
    loop=0,
    quality=100,
)
