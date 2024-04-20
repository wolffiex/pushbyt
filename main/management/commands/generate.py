from typing import Optional
import os
import tempfile
import subprocess
from PIL import Image
from datetime import datetime, timedelta
from django_rich.management import RichCommand
from main.animation.rays2 import clock_rays
from pathlib import Path
from django.utils import timezone
from main.models import Animation

FRAME_TIME = timedelta(milliseconds=100)
ANIM_DURATION = timedelta(seconds=15)
FRAME_COUNT = ANIM_DURATION / FRAME_TIME

RENDER_DIR = Path("render")


class Command(RichCommand):
    help = "Updates animation table"

    def handle(self, *args, **options):
        try:
            start_time = self.get_next_animation_time()
            if start_time:
                os.makedirs(RENDER_DIR, exist_ok=True)
                self.create_animations(start_time)
        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

    def get_next_animation_time(self) -> Optional[datetime]:
        now = timezone.localtime()
        second = now.second

        if 0 <= second < 15:
            next_second = 15
        elif 15 <= second < 30:
            next_second = 30
        elif 30 <= second < 45:
            next_second = 45
        else:
            next_second = 0
            now += timedelta(minutes=1)

        return now.replace(second=next_second, microsecond=0)

    def create_animations(self, start_time: datetime):
        end_time = start_time + timedelta(minutes=5)
        self.console.print(start_time)
        frames = clock_rays()
        next(frames)
        t = start_time
        animations = []
        while t < end_time:
            anim_frames = []
            anim_start_time = t
            for _ in range(int(FRAME_COUNT)):
                time_str = t.strftime("%-I:%M")
                anim_frames.append(frames.send(time_str))
                t += FRAME_TIME
            file_path = (
                Path("render") / anim_start_time.strftime("%j-%H-%M-%S")
            ).with_suffix(".webp")
            self.render(anim_frames, file_path)
            animations.append(
                Animation(
                    file_path=file_path,
                    start_time=anim_start_time,
                )
            )
        Animation.objects.bulk_create(animations)

    def render(self, frames, file_path):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            in_files = [
                self.convert_frame(temp_path, i, frame)
                for i, frame in enumerate(frames)
            ]
            frames_arg = " ".join(
                f"-frame {tf} +{FRAME_TIME.total_seconds() * 1000}" for tf in in_files
            )
            cmd = (
                f"webpmux {frames_arg} -loop 1 -bgcolor 255,255,255,255 -o {file_path}"
            )
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)

    def convert_frame(
        self, frame_dir: Path, frame_num: int, frame: Image.Image
    ) -> Path:
        frame_file = frame_dir / f"frame{frame_num:04d}.webp"
        frame.save(frame_file, "WebP", quality=100)
        return frame_file
