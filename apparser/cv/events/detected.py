from apparser.cv.events.base import CvEvent


class Detected(CvEvent):
    """Represent a newly detected object."""

    def __str__(self) -> str:
        """Return the event name.

        :return: Detected event name.
        :rtype: str
        """
        return "Detected"
