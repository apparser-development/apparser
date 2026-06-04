from __future__ import annotations

import uuid
import wave
from pathlib import Path


def create_wave_file(
    path: Path,
    frames: bytes,
    sample_width: int,
    channels: int = 1,
    sample_rate: int = 16_000,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as file:
        file.setnchannels(channels)
        file.setsampwidth(sample_width)
        file.setframerate(sample_rate)
        file.writeframes(frames)
    return path


def create_temp_audio_path(name: str) -> Path:
    base_dir = Path(__file__).resolve().parents[1] / "_tmp"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir / f"{uuid.uuid4().hex}_{name}"
