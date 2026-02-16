from apparser.cv.events.base import CvEvent


class UnDetected(CvEvent):
    def __str__(self) -> str:
        return "UnDetected"