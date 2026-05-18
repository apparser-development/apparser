"""Base interfaces for computer vision event handlers."""

import abc
from typing import Type

from apparser.cv.events import CvEvent
from apparser.cv.models import CvChangeData


class CvHandlers(abc.ABC):
    """Define the interface for computer vision event handler registries."""

    @abc.abstractmethod
    def register_handler(self, event: Type[CvEvent]):
        """Return a decorator that registers a handler for an event.

        :param event: Event type to subscribe to.
        :type event: Type[CvEvent]
        """
        pass

    @abc.abstractmethod
    def call(self, event: Type[CvEvent], changed_data: CvChangeData, *args):
        """Call handlers registered for the provided event.

        :param event: Event type to dispatch.
        :type event: Type[CvEvent]
        :param changed_data: Event payload with current and previous box data.
        :type changed_data: CvChangeData
        :param args: Additional context passed to handler functions.
        """
        pass
