import os
import subprocess
import base64
import tempfile
from rich import print
from rich.table import Table
from django_rich.management import RichCommand
from main.animation.rays import clock_rays
from io import BytesIO
import requests
from pathlib import Path

FRAME_TIME = 100
TIDBYT_API_PUSH = "https://api.tidbyt.com/v0/devices/%s/push"
DIST_DIR = Path("dist")
class Command(RichCommand):
    help = 'pushes animation to device'

    def add_arguments(self, parser):
        parser.add_argument('device_id', type=str, help='Device ID')

    def handle(self, *args, **options):
        print("[bold magenta]:ship: DEPLOY[/bold magenta]")
        try:
            frames = clock_rays()
            webp_files = self.render(frames)
            for i, webp in enumerate(webp_files):
                with open(webp, 'rb') as file:
                    # self.push(file.read(), options['device_id'], 'pb{i}', i == 0)
                    pass

        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

    def push(self, image_bytes, device_id, installation_id, background):
        api_token = os.getenv("TIDBYT_TOKEN")

        if not api_token:
            raise ValueError(f"Blank Tidbyt API token (set TIDBYT_TOKEN)")

        payload = {
            "deviceID": device_id,
            "image": base64.b64encode(image_bytes).decode("utf-8"),
            "installationID": installation_id,
            "background": background,
        }

        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.post(TIDBYT_API_PUSH % device_id, json=payload, headers=headers)

        if response.status_code != 200:
            self.console.print(f"Tidbyt API returned status {response.status_code}")
            self.console.print(response.text)
        else:
            ground = "Background" if background else "Foreground"
            self.console.print(f":green_circle: [green] Sent {installation_id} in {ground} [/green]")

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
