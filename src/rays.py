from PIL import Image, ImageDraw
import math
import os
import random
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def to_tuple(self):
        return (self.x, self.y)

WIDTH, HEIGHT = 64, 32
FRAME_DURATION = 100  # ms per frame (10fps)
SCALE_FACTOR = 4
CENTER = Point(SCALE_FACTOR * (WIDTH - 1) / 2, SCALE_FACTOR * (HEIGHT - 1) / 2)
SCALED_WIDTH, SCALED_HEIGHT = SCALE_FACTOR * WIDTH, SCALE_FACTOR * HEIGHT


image = Image.new("RGB", (WIDTH, HEIGHT), color="black")
frames = [Image.new("RGB", (WIDTH, HEIGHT), color="black")]



@dataclass
class Ray:
    angle: float
    _start: float = 0.0
    _end: float = 0.1

    @classmethod
    def new(cls):
        angle = random.uniform(0, 2 * math.pi)
        return Ray(angle)

    def to_line(self):
        return [self.start.to_tuple(), self.end.to_tuple()]

    def is_in_bounds(self):
        return self.start.x >=0 and self.start.x < SCALED_WIDTH and self.start.y >=0 and self.start.y < SCALED_HEIGHT

    def animate(self):
        self._start += 0.03
        self._end += 0.04

    @property
    def start(self):
        return self._to_point(self._start)

    @property
    def end(self):
        return self._to_point(self._end)

    def _to_point(self, percent):
        x = CENTER.x + SCALED_WIDTH * percent * math.cos(self.angle)
        y = CENTER.y + SCALED_WIDTH * percent * math.sin(self.angle)
        return Point(x, y)


frames = []
for _ in range(20):
    ray = Ray.new()
    color = (255, 150, 150)
    while ray.is_in_bounds():
        image = Image.new("RGB", (SCALED_WIDTH, SCALED_HEIGHT), color="black")
        draw = ImageDraw.Draw(image)
        color = tuple(max(0, min(255, a + b)) for a, b in zip(color, (-10, 0, 10)))
        assert len(color) == 3
        draw.line(ray.to_line(), fill=color, width=SCALE_FACTOR)
        # Downsample the high-resolution image to the desired size
        image_lo = image.resize((WIDTH, HEIGHT), resample=Image.LANCZOS)
        frames.append(image_lo)
        ray.animate()
        # i += 1
        # if i > 10:
        #     break

os.makedirs("dist", exist_ok=True)
frames[0].save(
    "dist/animation.webp",
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DURATION,
    loop=0,
    quality=100,
)
