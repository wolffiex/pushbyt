import tempfile
import subprocess
import os
from pathlib import Path
from PIL import Image
from rich.console import Console

console = Console()
sprites = Path("./sprites")
frame_files = [f for f in sorted(os.listdir(sprites)) if f.startswith("frame")]

def convert_image(file):
    png_image = Image.open(sprites / file)
    temp_file = tempfile.NamedTemporaryFile(suffix=".webp", delete=True)
    png_image.save(temp_file.name, "WebP")
    return temp_file

tempfiles = [convert_image(file) for file in frame_files]
frames = " ".join(f'-frame {f.name} +1000' for f in tempfiles)
print(frames)
cmd = f"webpmux {frames} -loop 10 -bgcolor 255,255,255,255 -o out.webp"
print(cmd)
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
