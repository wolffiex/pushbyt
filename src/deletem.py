import requests
import os
import argparse
from rich.console import Console

console = Console()
parser = argparse.ArgumentParser(description="Render a Pixlet script and push the WebP output to a Tidbyt")
parser.add_argument("device_id", help="Tidbyt device ID")
args = parser.parse_args()

TIDBYT_API = "https://api.tidbyt.com/v0/"
api_token = os.getenv("TIDBYT_TOKEN")

if not api_token:
    raise ValueError(f"Blank Tidbyt API token (set TIDBYT_TOKEN)")

base_url = TIDBYT_API + f"devices/{args.device_id}/installations/"

headers = {"Authorization": f"Bearer {api_token}"}
for i in range(5):

    url = base_url + f"id{i:02d}"
    console.print(url)

    response = requests.delete(url, headers=headers)

    if response.status_code != 200:
        print(f"Tidbyt API returned status {response.status_code}")
        print(response.text)
        raise ValueError(f"Tidbyt API returned status: {response.status_code}")
