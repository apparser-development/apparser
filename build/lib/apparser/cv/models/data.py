from dataclasses import dataclass
from typing import Type

from apparser.core import BaseUi
from apparser.cv.events import CvEvent


@dataclass(frozen=True)
class CvBox:
    class_name: str
    track_id: int | None
    x: int
    y: int
    width: int
    height: int
    ui: BaseUi

@dataclass(frozen=True)
class CvChangeData:
    event: Type[CvEvent]
    box: CvBox
    old_box: CvBox


@dataclass(frozen=True)
class CvAllData:
    boxes: list[CvBox]
