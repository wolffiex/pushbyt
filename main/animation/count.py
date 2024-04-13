import argparse
import base64
import os
import requests


TIDBYT_API_PUSH = "https://api.tidbyt.com/v0/devices/%s/push"
def push(file, device_id, installation_id, background):
    api_token = os.getenv("TIDBYT_TOKEN")

    if not api_token:
        raise ValueError(f"Blank Tidbyt API token (set TIDBYT_TOKEN)")

    with open(file, "rb") as image_file:
        print(f"{file}  {installation_id}")
        image = image_file.read()

        payload = {
            "deviceID": device_id,
            "image": base64.b64encode(image).decode("utf-8"),
            "installationID": installation_id,
            "background": background,
        }

        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.post(TIDBYT_API_PUSH % device_id, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"Tidbyt API returned status {response.status_code}")
            print(response.text)
            raise ValueError(f"Tidbyt API returned status: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render a Pixlet script and push the WebP output to a Tidbyt")
    parser.add_argument("device_id", help="Tidbyt device ID")
    args = parser.parse_args()
    for i in range(5):
        file_name = f"dist/out_{i:02d}.webp" 
        installation_id = f"id{i:02d}"
        push(file_name, args.device_id, installation_id, i != 0)
