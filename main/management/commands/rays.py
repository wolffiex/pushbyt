import subprocess
from PIL import Image
from typing import Optional, List
import tempfile
from datetime import datetime, timedelta, time
from django_rich.management import RichCommand
from main.animation.rays2 import clock_rays
from pathlib import Path
import itertools
from django.utils import timezone
from main.models import Animation
import os

FRAME_TIME = timedelta(milliseconds=100)
DURATION = timedelta(seconds=15)
FRAME_COUNT = DURATION / FRAME_TIME


def time_to_str(t:time):
    return t.strftime("%-I:%M")

class Command(RichCommand):
    help = "Renders rays clock"

    def handle(self, *args, **options):
        frames = clock_rays()
        next(frames)
        try:
            os.makedirs("dist/rays", exist_ok=True)
            for hour in range(1, 13):
                for minute in range(0, 60):
                    time_str = f"{hour}:{minute}"
                    # each minute divided into 4 parts of 15 seconds
                    for part in range(0, 3):
                        anim_file = Path("dist/rays") / f"ray-{hour:02d}-{minute:02d}-{part}.webp"
                        anim_frames = []
                        for _ in range(int(FRAME_COUNT)):
                            anim_frames.append(frames.send(time_str))
                        self.render(anim_file, anim_frames)
                        self.console.print(anim_file)
        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

    def get_next_animation_time(self) -> Optional[datetime]:
        return timezone.localtime()

    def render(self, anim_file: Path, frames:List[Image.Image]):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            in_files = [
                self.convert_frame(temp_path, i, frame)
                for i, frame in enumerate(frames)
            ]
            frames_arg = " ".join(
                f"-frame {tf} +{FRAME_TIME.total_seconds() * 1000}" for tf in in_files
            )
            cmd = f"webpmux {frames_arg} -loop 1 -bgcolor 255,255,255,255 -o {anim_file}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)

    def convert_frame(
        self, frame_dir: Path, frame_num: int, frame: Image.Image
    ) -> Path:
        frame_file = frame_dir / f"frame{frame_num:04d}.webp"
        frame.save(frame_file, "WebP", quality=100)
        return frame_file
