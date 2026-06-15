from apparser.cv.events.base import CvEvent


class Undetected(CvEvent):
    """Represent a previously tracked object that disappeared."""

    def __str__(self) -> str:
        """Return the event name.

        :return: Undetected event name.
        :rtype: str
        """
        return "UnDetected"
