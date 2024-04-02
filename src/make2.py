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
    text = f"{num:04d}"
    position = (10, 10)
    draw = ImageDraw.Draw(image)
    draw.text(position, text, font=font, fill=(255, 255, 255))
    return image

frame_time = 100
images = [make_frame(n) for n in range(1,150)]
tempfiles = [convert_image(image) for image in images]
frames = " ".join(f'-frame {f.name} +{frame_time}' for f in tempfiles)
cmd = f"webpmux {frames} -loop 10 -bgcolor 255,255,255,255 -o out.webp"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Check the return code
if result.returncode != 0:
    console.print("Command execution failed", style="red")
    print(result.stderr)

for temp_file in tempfiles:
    temp_file.close()

# print(webpmux_animate(input_images=tempfiles, output_image="anim_container.webp",
#                       loop="10", bgcolor="255,255,255,255"))


# webpmux  -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp_bp7j2zq.webp +100 
#           -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp2c4idylv.webp +100
#           -fram /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmpx821h6zz.webp +100 
#           -loop 10 -bgcolor 255,255,255,255 -o anim_container.webp
