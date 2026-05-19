from apparser.cv.events.base import CvEvent


class Resized(CvEvent):
    """Represent a detected object whose size changed."""

    def __str__(self) -> str:
        """Return the event name.

        :return: Resized event name.
        :rtype: str
        """
        return "Resized"
