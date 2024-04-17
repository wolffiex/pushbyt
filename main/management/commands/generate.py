import os
import subprocess
import base64
import tempfile
from django_rich.management import RichCommand
from main.animation.rays import clock_rays
import requests
from datetime import datetime
import pytz

FRAME_TIME = 100
class Command(RichCommand):
    help = 'Updates animation table'

    def handle(self, *args, **options):
        try:
            los_angeles_tz = pytz.timezone('America/Los_Angeles')
            frames = clock_rays(datetime.now(los_angeles_tz))
            webp_files = self.render(frames)
            for i, webp in enumerate(webp_files):
                with open(webp, 'rb') as file:
                    self.push(file.read(), options['device_id'], f'pb{i}', i != 0)

        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

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
