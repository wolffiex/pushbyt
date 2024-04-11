from PIL import Image, ImageDraw, ImageFont
import math
import os
import random
from dataclasses import dataclass
from typing import List

width, height = 64, 32
frames = []
duration = 100  # ms per frame (10fps)


def generate_coordinates(right, bottom):
    return ((x, y) for x in range(right) for y in range(bottom))


text = "12:45"
text_color = (255, 0, 0)  # Red color
image = Image.new("RGB", (width, height), color="black")
font = ImageFont.truetype("./fonts/pixelmix/pixelmix.ttf", 8)
draw = ImageDraw.Draw(image)
text_position = (0, 0)
bbox = draw.textbbox(text_position, text, font=font)
draw.text(text_position, text, font=font, fill="white")
left, top, right, bottom = bbox
pixels = image.load()
print("Bounding box coordinates (left, top, right, bottom):", bbox)
# pixels_on = ((x, y) for x in range(right) for y in range(bottom) if pixels[x, y] != (0, 0, 0))
frames = [Image.new("RGB", (width, height), color="black")]


@dataclass
class Star:
    angle: float
    x: float
    y: float
    velocity: float
    MAX_STARS = 100

    @property
    def ix(self):
        return round(self.x)

    @property
    def iy(self):
        return round(self.y)

    def is_in_bounds(self):
        return self.ix >=0 and self.ix < width and self.iy >=0 and self.iy < height
    
    def move(self):
        self.x = self.x + math.cos(self.angle) * self.velocity
        self.y = self.y + math.sin(self.angle) * self.velocity

    @staticmethod
    def maybe_generate(n):
        if n < 0:
            raise ValueError("Input must be a non-negative integer.")

        probability = 1 / (
            1 + math.exp(n * (math.log(Star.MAX_STARS) / Star.MAX_STARS))
        )
        if random.random() < probability:
            # Generate a random angle in radians
            return Star.generate()

    @classmethod
    def generate(cls):
        angle = random.uniform(0, 2 * math.pi)
        x, y = cls.get_start(angle)
        return cls(angle, x, y, 2)  # random.uniform(0.5, 3))

    @staticmethod
    def get_start(angle):
        if 0 <= angle < math.pi / 2:
            return 32, 15
        elif math.pi / 2 <= angle < math.pi:
            return 31, 15
        elif math.pi <= angle < 3 * math.pi / 2:
            return 31, 16
        else:
            return 32, 16

    def __repr__(self):
        return f"Star({self.x}, {self.y})"

stars : List[Star] = []
for _ in range(200):
    frame = Image.new("RGB", (width, height), color="black")
    stars = [star for star in stars if star.is_in_bounds()]
    for _ in range(3):
        # maybe_star = Star.maybe_generate(len(stars))
        maybe_star = Star.generate()
        if maybe_star:
            stars.append(maybe_star)
    for star in stars:
        frame.putpixel((star.ix, star.iy), (255, 255, 255))
        # frame.putpixel((15, 22), (255, 255, 255))
        star.move()
    frames.append(frame)

for _ in range(20):
    frames.append(frames[0])

os.makedirs("dist", exist_ok=True)
frames[0].save(
    "dist/animation.webp",
    save_all=True,
    append_images=frames[1:],
    duration=duration,
    loop=0,
    quality=100,
)
