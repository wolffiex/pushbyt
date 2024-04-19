import subprocess
from PIL import Image
from typing import Optional, List
import tempfile
from datetime import datetime, timedelta
from django_rich.management import RichCommand
from main.animation.rays2 import clock_rays
from pathlib import Path
import itertools
import pytz
import aiofiles
import asyncio
from asgiref.sync import async_to_sync

FRAME_TIME = timedelta(milliseconds=100)
DURATION = timedelta(seconds=15)
FRAME_COUNT = DURATION / FRAME_TIME


class Command(RichCommand):
    help = "Updates animation table"

    def handle(self, *args, **options):
        try:
            anim_files = self.create_animations()
            self.console.print(anim_files)
        except Exception as e:
            self.console.print_exception(show_locals=True)
            raise e

    @async_to_sync
    async def create_animations(self) -> List[Path]:
        start_time = self.get_next_animation_time()
        if not start_time:
            return list()
        end_time = start_time + timedelta(minutes=5)
        los_angeles_tz = pytz.timezone("America/Los_Angeles")
        localized_time = los_angeles_tz.localize(start_time)
        frames = clock_rays(datetime.now(los_angeles_tz), FRAME_TIME)
        anim_tasks = []
        anim_time = start_time
        while anim_time < end_time:
            anim_tasks.append(self.render(list(itertools.islice(frames, int(FRAME_COUNT)))))
            anim_time += DURATION

        webp_files = self.render(frames)
        for i, webp in enumerate(webp_files):
            with open(webp, "rb") as file:
                self.push(file.read(), options["device_id"], f"pb{i}", i != 0)

    async def render(self, frames):
        convert_tasks = [asyncio.create_task(self.convert_frame(i, frame)) for i,frame in enumerate(frames)]
        in_files = await asyncio.gather(*convert_tasks)
        with tempfile.NamedTemporaryFile(suffix=".webp", delete=False) as temp_file:
            out_file = temp_file.name
        frames_arg = " ".join(f"-frame {tf} +{FRAME_TIME}" for tf in in_files)
        cmd = f"webpmux {frames_arg} -loop 1 -bgcolor 255,255,255,255 -o {out_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        with open(out_file, "rb") as file:
            file_bytes = file.read()

        removal_tasks = [
            asyncio.create_task(remove_temp_file(temp_file))
            for temp_file in in_files + [out_file]
        ]
        await asyncio.gather(*removal_tasks)

        return file_bytes

    def get_next_animation_time(self) -> Optional[datetime]:
        pass

    async def convert_frame(self, frame_num:int, frame:Image.Image):
        async with aiofiles.tempfile.NamedTemporaryFile(
            suffix=".webp", delete=False
        ) as temp_file:
            frame_name = temp_file.name
        frame.save(frame_name, "WebP", quality=100)
        return frame_name

    async def remove_temp_file(self, temp_file):
        await aiofiles.os.unlink(temp_file)
