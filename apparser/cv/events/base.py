"""Base types for computer vision events."""

import abc


class CvEvent(abc.ABC):
    """Define the interface for computer vision change events."""

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return the human-readable event name.

        :return: Event name.
        :rtype: str
        """
        raise NotImplementedError()
