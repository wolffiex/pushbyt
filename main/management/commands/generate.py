import subprocess
from PIL import Image
from typing import Optional, Generator
import tempfile
from datetime import datetime, timedelta
from django_rich.management import RichCommand
from main.animation.rays2 import clock_rays
from pathlib import Path
import itertools
import pytz
from django.utils import timezone

FRAME_TIME = timedelta(milliseconds=100)
DURATION = timedelta(seconds=11)
FRAME_COUNT = DURATION / FRAME_TIME


class Command(RichCommand):
    help = "Updates animation table"

    def handle(self, *args, **options):
        try:
            start_time = self.get_next_animation_time()
            if start_time:
                for anim_file in self.create_animations(start_time):
                    self.console.print(anim_file)
        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

    def get_next_animation_time(self) -> Optional[datetime]:
        return timezone.localtime()

    def create_animations(self, start_time: datetime) -> Generator[Path, None, None]:
        end_time = start_time + timedelta(minutes=1)
        self.console.print(start_time)
        frames = clock_rays(start_time, FRAME_TIME)
        anim_time = start_time
        while anim_time < end_time:
            yield self.render(list(itertools.islice(frames, int(FRAME_COUNT))))
            anim_time += DURATION

    def render(self, frames) -> Path:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            in_files = [
                self.convert_frame(temp_path, i, frame)
                for i, frame in enumerate(frames)
            ]
            with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as temp_file:
                out_file = temp_file.name
            frames_arg = " ".join(
                f"-frame {tf} +{FRAME_TIME.total_seconds() * 1000}" for tf in in_files
            )
            cmd = f"webpmux {frames_arg} -loop 1 -bgcolor 255,255,255,255 -o {out_file}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(result.stderr)
            return Path(out_file)

    def convert_frame(
        self, frame_dir: Path, frame_num: int, frame: Image.Image
    ) -> Path:
        frame_file = frame_dir / f"frame{frame_num:04d}.webp"
        frame.save(frame_file, "WebP", quality=100)
        return frame_file
