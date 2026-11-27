#!/usr/bin/env python3
"""Extract full-size reference JPEGs at explicit times in a local video."""

import argparse
from decimal import Decimal
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory


def timestamp_ms(text):
    if not re.fullmatch(r"[0-9]+(?::[0-9]+){0,2}(?:\.[0-9]{1,3})?", text):
        raise argparse.ArgumentTypeError(f"时间点格式无效：{text}")
    whole, _, fraction = text.partition(".")
    parts = [int(part) for part in whole.split(":")]
    if any(part >= 60 for part in parts[1:]):
        raise argparse.ArgumentTypeError(f"时间点中的分或秒超出范围：{text}")
    seconds = 0
    for part in parts:
        seconds = 60 * seconds + part
    return seconds * 1000 + int(fraction.ljust(3, "0"))


def duration_ms(video):
    output = subprocess.check_output([
        "ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
        "-select_streams", "V:0", "-show_entries", "stream=duration:format=duration",
        "-of", "json", str(video),
    ])
    metadata = json.loads(output)
    if not metadata.get("streams"):
        raise ValueError("文件中没有可取帧的视频轨道")
    for section in (metadata["streams"][0], metadata.get("format", {})):
        duration = section.get("duration")
        if duration and duration != "N/A":
            seconds = Decimal(duration)
            if seconds.is_finite() and seconds > 0:
                return seconds * 1000
    raise ValueError("无法从本地文件读取视频时长")


def extract_frames(video, directory, times):
    for program in ("ffprobe", "ffmpeg"):
        if not shutil.which(program):
            raise ValueError(f"缺少 {program}，请使用已安装 FFmpeg 的环境")
    video = video.resolve(strict=True)
    if not video.is_file():
        raise ValueError(f"需要本地视频文件：{video}")
    limit = duration_ms(video)
    outputs = {}
    for ms in times:
        if ms >= limit:
            raise ValueError(f"{ms} 毫秒超出范围，视频时长为 {limit.normalize():f} 毫秒")
        destination = directory / f"frame-{ms:09d}ms.jpg"
        if os.path.lexists(destination):
            raise FileExistsError(f"文件已存在：{destination}")
        outputs[ms] = destination

    directory.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".extract-frames-", dir=directory) as staging:
        for ms, destination in outputs.items():
            staged = Path(staging) / destination.name
            # Decode from the preceding keyframe and keep the frame visible at this instant.
            subprocess.run([
                "ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe",
                "-ss", f"{ms // 1000}.{ms % 1000:03d}", "-noaccurate_seek", "-i", str(video),
                "-map", "0:V:0", "-vf", "trim=end_pts=1,setpts=PTS-STARTPTS",
                "-fps_mode", "passthrough", "-update", "1", "-q:v", "2", str(staged),
            ], check=True)
            if not staged.is_file() or not staged.stat().st_size:
                raise ValueError(f"无法读取 {ms} 毫秒处的画面")
        for destination in outputs.values():
            # A hard link publishes a complete image and fails if another process created it.
            os.link(Path(staging) / destination.name, destination)
            print(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path, metavar="VIDEO")
    parser.add_argument("directory", type=Path, metavar="OUTPUT_DIR")
    parser.add_argument("times", type=timestamp_ms, nargs="+", metavar="TIME",
                        help="秒、分:秒或时:分:秒，可带最多三位小数")
    args = parser.parse_args()
    try:
        extract_frames(args.video, args.directory, args.times)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{parser.prog}: {error}\n")
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
