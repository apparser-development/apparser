from dataclasses import dataclass
from typing import Type

from apparser.core import Ui
from apparser.cv.events import CvEvent


@dataclass(frozen=True)
class CvBox:
    class_name: str
    class_id: int
    x: int
    y: int
    width: int
    height: int
    ui: Ui

@dataclass(frozen=True)
class CvChangeData:
    event: Type[CvEvent]
    box: CvBox
    old_box: CvBox


@dataclass(frozen=True)
class CvAllData:
    boxes: list[CvBox]
