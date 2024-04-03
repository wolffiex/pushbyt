import tempfile
import subprocess
import os
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from rich.console import Console

console = Console()
font = ImageFont.truetype("./fonts/pixelmix/pixelmix.ttf", 8)

def convert_image(image):
    temp_file = tempfile.NamedTemporaryFile(suffix=".webp", delete=True)
    image.save(temp_file.name, "WebP", quality=100)
    return temp_file

def make_frame(num):
    # Create a new image with a black background
    width, height = 64, 32
    image = Image.new("RGB", (width, height), "black")
    text = f"dy{num:04d}"
    position = (10, 10)
    draw = ImageDraw.Draw(image)
    draw.text(position, text, font=font, fill=(255, 255, 255))
    return image

# https://developers.google.com/speed/webp/docs/webpmux
frame_time = 100
frame_ranges = [range(i * 150, (i + 1) * 150) for i in range(5)]
for i, fr in enumerate(frame_ranges):
    images = [make_frame(n+1) for n in fr]
    tempfiles = [convert_image(image) for image in images]
    frames = " ".join(f'-frame {f.name} +{frame_time}' for f in tempfiles)
    outname = f"dist/out_{i:02d}.webp"
    cmd = f"webpmux {frames} -loop 1 -bgcolor 255,255,255,255 -o {outname}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # Check the return code
    if result.returncode != 0:
        console.print("Command execution failed", style="red")
        print(result.stderr)
        exit(1)

    for temp_file in tempfiles:
        temp_file.close()
