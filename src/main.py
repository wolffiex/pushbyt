import argparse
from webptools import webpmux_animate
import base64
import os
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path
import tempfile


TIDBYT_API_PUSH = "https://api.tidbyt.com/v0/devices/%s/push"
sprites = Path("./sprites")
frame_files = [f for f in sorted(os.listdir(sprites)) if f.startswith("frame")]

tempfiles = []
for file in frame_files:
    png_image = Image.open(sprites / file)
    with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as temp_file:
        # Save the image as WebP format
        png_image.save(temp_file.name, "WebP")
        tempfiles.append(temp_file.name +" +100")

# print(webpmux_animate(input_images=tempfiles, output_image="anim_container.webp",
#                       loop="10", bgcolor="255,255,255,255"))

frames = " ".join(f'-frame {f}' for f in tempfiles)
cmd = f"webpmux {frames} -loop 10 -bgcolor 255,255,255,255 -o out.webp"
print(cmd)

# webpmux  -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp_bp7j2zq.webp +100 
#           -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmp2c4idylv.webp +100
#           -frame /var/folders/3v/jl2nyhvx0fv2qfy6yz4fh9cw0000gn/T/tmpx821h6zz.webp +100 
#           -loop 10 -bgcolor 255,255,255,255 -o anim_container.webp
def push(device_id, installation_id, background):
    api_token = os.getenv("TIDBYT_TOKEN")

    if not api_token:
        raise ValueError(f"Blank Tidbyt API token (set TIDBYT_TOKEN)")

    # Get the image data from the BytesIO object
    image_data = create()

    payload = {
        "deviceID": device_id,
        "image": base64.b64encode(image_data).decode("utf-8"),
        "installationID": installation_id,
        "background": background,
    }

    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.post(TIDBYT_API_PUSH % device_id, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Tidbyt API returned status {response.status_code}")
        print(response.text)
        raise ValueError(f"Tidbyt API returned status: {response.status_code}")

def create():
    with open("out.webp", "rb") as anim:
        return anim.read()
    # Create a new image with a black background
    width, height = 64, 32
    image = Image.new("RGB", (width, height), "black")

    # Get the pixel data
    pixels = image.load()

    # Draw a 10x10 white box offset by 10 pixels on each axis
    for i in range(10, 20):
        for j in range(10, 20):
            pixels[i, j] = (255, 0, 0)  # Set pixel to white

    png_image = Image.open("sprites/Sprite.png")

    # Create a new list to store the frames
    frames = [image, png_image]

    # Save the frames as an animated WebP to a BytesIO object
    image_buffer = BytesIO()
    frames[0].save(
        image_buffer,
        "WebP",
        save_all=True,
        append_images=frames[1:],
        duration=1000,  # Duration of each frame in milliseconds
        loop=0,  # Set the loop count (0 for infinite loop)
    )

    # Save the image to a BytesIO object
    image_buffer = BytesIO()
    image.save(image_buffer, "WebP")
    return image_buffer.getvalue()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a Pixlet script and push the WebP output to a Tidbyt")
    parser.add_argument("device_id", help="Tidbyt device ID")
    parser.add_argument("-i", "--installation-id", help="Give your installation an ID to keep it in the rotation")
    parser.add_argument("-b", "--background", action="store_true", help="Don't immediately show the image on the device")
    args = parser.parse_args()

    push(args.device_id, args.installation_id, args.background)


# pass input_images(.webp image) path with FRAME_OPTIONS, as array,ouput image will be animated .webp image

# https://developers.google.com/speed/webp/docs/webpmux
# FRAME_OPTIONS

# -file_i +di[+xi+yi[+mi[bi]]]

# e.g -frame one.webp +100 -frame two.webp +100+50+50 -frame three.webp +100+50+50+1+b

# Where: file_i is the i'th frame (WebP format), xi,yi specify the image offset for this frame,
# di is the pause duration before next frame, mi is the dispose method for this frame (0 for NONE or 1 for BACKGROUND)
# and bi is the blending method for this frame (+b for BLEND or -b for NO_BLEND).
# Argument bi can be omitted and will default to +b (BLEND). Also, mi can be omitted if bi is omitted and
# will default to 0 (NONE). Finally,
# if mi and bi are omitted then xi and yi can be omitted and will default to +0+0.

# -loop n

# e.g 10

# Loop the frames n number of times. 0 indicates the frames should loop forever.
# Valid range is 0 to 65535 [Default: 0 (infinite)].

# -bgcolor A,R,G,B

# e.g 255,255,255,255

# Background color of the canvas. Where: A, R, G and B are integers in the range 0 to 255 specifying
# the Alpha, Red, Green and Blue component values respectively [Default: 255,255,255,255].

# now read anim_container file and return as BtyesIO

