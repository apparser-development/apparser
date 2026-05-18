"""Data models describing computer vision detections and changes."""

from dataclasses import dataclass
from typing import Type

from apparser.core import BaseUi
from apparser.cv.events import CvEvent


@dataclass(frozen=True)
class CvBox:
    """Store a detected object bounding box and its UI context."""

    class_name: str
    track_id: int | None
    x: int
    y: int
    width: int
    height: int
    ui: BaseUi

@dataclass(frozen=True)
class CvChangeData:
    """Store an event together with current and previous box states."""

    event: Type[CvEvent]
    box: CvBox
    old_box: CvBox


@dataclass(frozen=True)
class CvAllData:
    """Store all detected boxes for a single computer vision read."""

    boxes: list[CvBox]
