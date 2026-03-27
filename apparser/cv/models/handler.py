from dataclasses import dataclass
from typing import Callable, Optional, Type

from apparser.cv.events import CvEvent
from apparser.cv.models import CvAllData, CvClassData
from apparser.core import Ui


@dataclass(frozen=True)
class CvHandler:
    event: Type[CvEvent]
    function: Callable[[Optional[CvAllData], Optional[Ui], Optional[CvClassData]], None]
