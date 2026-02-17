from typing import Callable

from apparser.cv.handlers.base import CvHandler
from apparser.cv.events import CvEvent


class DefaultHandler(CvHandler):
    def __init__(self):
        raise NotImplementedError()

    def register_event(self, event: CvEvent, function: Callable):
        if not isinstance(event, CvEvent):
            raise TypeError("event must be a apparser.cv.events.CvEvent")
        
        raise NotImplementedError()

    def call(self, event, data):
        return super().call(event, data)