from PIL import Image, ImageDraw
import math
import os
from dataclasses import dataclass
import tempfile
import subprocess

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

STEPS = 200
SCALE_FACTOR = 4
center = SCALE_FACTOR * (width - 1) / 2, SCALE_FACTOR * (height - 1) / 2
scaled = SCALE_FACTOR * width, SCALE_FACTOR * height
for step in range(STEPS):
    angle = 2 * math.pi * step / 100
    image = Image.new("RGB", scaled, color="black")
    draw = ImageDraw.Draw(image)

    length = 64 * SCALE_FACTOR  # somewhat arbirary chosen to extend beyond boundary
    end = center[0] + length * math.cos(angle), center[1] + length * math.sin(angle)

    draw.line([center, end], fill="white", width=SCALE_FACTOR)

    # Downsample the high-resolution image to the desired size
    image_lo = image.resize((width, height), resample=Image.LANCZOS)

    frames.append(image_lo)

os.makedirs("dist", exist_ok=True)
frames[0].save(
    "dist/animation2.webp",
    save_all=True,
    append_images=frames[1:],
    duration=duration,
    loop=0,
    quality=100,
)

def convert_frame(self, frame):
    temp_file = tempfile.NamedTemporaryFile(suffix=".webp", delete=True)
    frame.save(temp_file.name, "WebP", quality=100)
    return temp_file

def render(self, frames):
    in_files = [self.convert_frame(frame) for frame in frames]
    out_files = []
    for i in range(4):
        out_file = DIST_DIR / f"render{i:02d}.webp" 
        out_files.append(out_file)
        start = i * 150
        end = start + 150
        frames_arg = " ".join(f'-frame {f.name} +{FRAME_TIME}' for f in in_files[start:end])
        cmd = f"webpmux {frames_arg} -loop 1 -bgcolor 255,255,255,255 -o {out_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

    for f in in_files:
        f.close()

    return out_files
