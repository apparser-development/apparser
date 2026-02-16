from apparser.cv.handlers.base import CvHandler

from apparser.cv.events import CvEvent
from apparser.cv.models import CvData


class DefaultHandler(CvHandler):
    def __init__(self):
        raise NotImplementedError()

    def register_event(self, event: CvEvent, data: CvData):
        if not isinstance(event, CvEvent):
            raise TypeError("event must be a apparser.cv.events.CvEvent")
        
        if not isinstance(data, CvData):
            raise TypeError("data must be a apparser.cv.models.CvData")
        
        raise NotImplementedError()