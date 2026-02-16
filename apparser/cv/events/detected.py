from apparser.cv.events.base import CvEvent


class Detected(CvEvent):
    def __str__(self) -> str:
        return "Detected"