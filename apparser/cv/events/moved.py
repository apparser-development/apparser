from apparser.cv.events.base import CvEvent


class Moved(CvEvent):
    """Represent a detected object whose position changed."""

    def __str__(self) -> str:
        """Return the event name.

        :return: Moved event name.
        :rtype: str
        """
        return "Moved"
