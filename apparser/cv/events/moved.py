from apparser.cv.events.base import CvEvent


class Moved(CvEvent):
    def __str__(self) -> str:
        return "Moved"