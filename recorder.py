"""Vibration-triggered audio/video recorder for a Raspberry Pi.

Recovered from a 2020 apartment ceiling-noise evidence project. An Arduino
samples a piezo sensor and streams peak vibration readings over USB serial.
The Raspberry Pi establishes a short baseline, then records a timestamped
camera/audio clip whenever a later reading exceeds that baseline.
"""

from __future__ import annotations

import argparse
from collections import deque
from datetime import datetime
from pathlib import Path
import subprocess
import time

import serial


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H_%M_%S")


def record_clip(
    output_dir: Path,
    camera: str,
    audio_device: str,
    duration: int,
    width: int,
    height: int,
    fps: int,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{timestamp()}.avi"

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "alsa",
        "-i",
        audio_device,
        "-itsoffset",
        "00:00:00",
        "-f",
        "video4linux2",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        camera,
        "-t",
        f"00:00:{duration:02d}",
        str(output),
    ]
    subprocess.run(command, check=True)
    return output


def monitor(args: argparse.Namespace) -> None:
    baseline: deque[int] = deque(maxlen=args.baseline_samples)

    with serial.Serial(args.serial_port, args.baud, timeout=5) as sensor:
        print(f"Listening on {args.serial_port} at {args.baud} baud")

        while True:
            raw = sensor.readline().decode(errors="ignore").strip()
            if not raw.isdigit():
                continue

            reading = int(raw)

            if len(baseline) < args.baseline_samples:
                baseline.append(reading)
                threshold = max(baseline)
                print(
                    f"Calibrating {len(baseline)}/{args.baseline_samples}: "
                    f"reading={reading}, threshold={threshold}"
                )
                continue

            threshold = max(baseline) + args.margin
            if reading <= threshold:
                continue

            print(f"Trigger: reading={reading} > threshold={threshold}")
            try:
                output = record_clip(
                    output_dir=args.output_dir,
                    camera=args.camera,
                    audio_device=args.audio_device,
                    duration=args.duration,
                    width=args.width,
                    height=args.height,
                    fps=args.fps,
                )
                print(f"Saved {output}")
            finally:
                sensor.reset_input_buffer()
                time.sleep(args.cooldown)
                sensor.reset_input_buffer()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serial-port", default="/dev/ttyACM0")
    parser.add_argument("--baud", type=int, default=9600)
    parser.add_argument("--camera", default="/dev/video0")
    parser.add_argument("--audio-device", default="default")
    parser.add_argument("--output-dir", type=Path, default=Path("video_export"))
    parser.add_argument("--baseline-samples", type=int, default=100)
    parser.add_argument("--margin", type=int, default=0)
    parser.add_argument("--duration", type=int, default=3)
    parser.add_argument("--cooldown", type=float, default=1.0)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--fps", type=int, default=25)
    return parser.parse_args()


if __name__ == "__main__":
    monitor(parse_args())