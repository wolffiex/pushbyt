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
    _end: float = 0.01
    color = (255, 150, 150)

    @classmethod
    def new(cls):
        angle = random.uniform(0, 2 * math.pi)
        return Ray(angle)

    def to_line(self):
        return [self.start.to_tuple(), self.end.to_tuple()]

    def is_in_bounds(self):
        return self.start.x >=0 and self.start.x < SCALED_WIDTH and self.start.y >=0 and self.start.y < SCALED_HEIGHT

    def animate(self):
        self._start += 0.04
        self._end += 0.06
        self.color = tuple(max(0, min(255, a + b)) for a, b in zip(self.color, (-10, 0, 10)))
        assert len(self.color) == 3

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
rays = []
for _ in range(500):
    num_rays = len(rays)
    if random.random() > num_rays / 10:
        rays.append(Ray.new())
    image = Image.new("RGB", (SCALED_WIDTH, SCALED_HEIGHT), color="black")
    draw = ImageDraw.Draw(image)
    for ray in rays:
        draw.line(ray.to_line(), fill=ray.color, width=SCALE_FACTOR)
        ray.animate()

    # Downsample the high-resolution image to the desired size
    image_lo = image.resize((WIDTH, HEIGHT), resample=Image.LANCZOS)
    frames.append(image_lo)
    rays = [ray for ray in rays if ray.is_in_bounds()]

os.makedirs("dist", exist_ok=True)
frames[0].save(
    "dist/animation.webp",
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DURATION,
    loop=0,
    quality=100,
)
