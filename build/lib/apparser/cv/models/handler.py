from dataclasses import dataclass
from typing import Callable, Optional, Type

from apparser.cv.events import CvEvent
from apparser.cv.models import CvAllData, CvChangeData
from apparser.core import BaseUi


@dataclass(frozen=True)
class CvHandler:
    event: Type[CvEvent]
    function: Callable[[Optional[CvAllData], Optional[BaseUi], Optional[CvChangeData]], None]
    class_name: str | None = None
