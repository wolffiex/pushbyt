import argparse
import base64
import json
import os
import requests
from io import BytesIO
from PIL import Image
import logging

TIDBYT_API_PUSH = "https://api.tidbyt.com/v0/devices/%s/push"

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
    # Create a new image with a black background
    width, height = 64, 32
    image = Image.new("RGB", (width, height), "black")

    # Get the pixel data
    pixels = image.load()

    # Draw a 10x10 white box offset by 10 pixels on each axis
    for i in range(10, 20):
        for j in range(10, 20):
            pixels[i, j] = (255, 0, 255)  # Set pixel to white

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

