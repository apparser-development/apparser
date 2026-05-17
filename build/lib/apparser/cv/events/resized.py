from apparser.cv.events.base import CvEvent


class Resized(CvEvent):
    def __str__(self) -> str:
        return "Resized"