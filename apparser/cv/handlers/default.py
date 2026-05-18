"""Default computer vision event handler registry."""

from typing import Callable, Type, Optional, Any
import inspect

from apparser.core import BaseUi
from apparser.cv.handlers.base import CvHandlers
from apparser.cv.events import CvEvent
from apparser.cv.models import CvAllData, CvHandler, CvChangeData


def _form_args(function: Callable, *args) -> dict[str, Any]:
    """Build keyword arguments matching the annotated handler signature.

    :param function: Handler function to inspect.
    :type function: Callable
    :param args: Available arguments for the handler call.
    :return: Keyword arguments matched by exact annotation type.
    :rtype: dict[str, Any]
    """
    result = {}
    function_signature = inspect.signature(function)
    for arg in function_signature.parameters.values():
        for a in args:
            if arg.annotation is type(a):
                result[arg.name] = a
    return result


class DefaultHandlers(CvHandlers):
    """Store and dispatch handlers for computer vision events."""

    def __init__(self):
        """Initialize an empty handler registry."""
        self.__events: list[CvHandler] = []

    def register_handler(self, event: Type[CvEvent], *args, class_name: str = None):
        """Create a decorator that registers a handler for an event.

        :param event: Event type to subscribe to.
        :type event: Type[CvEvent]
        :param args: Reserved positional arguments for compatibility.
        :param class_name: Optional object class filter for the handler.
        :type class_name: str | None
        :raises TypeError: If ``event`` is the abstract base event type.
        """
        if event is CvEvent:
            raise TypeError("event must be a apparser.cv.events.CvEvent")

        def decorator(function: Callable[[Optional[CvAllData], Optional[BaseUi], Optional[CvChangeData]], None]):
            """Register the decorated function as an event handler.

            :param function: Handler function to store.
            :type function: Callable[[Optional[CvAllData], Optional[BaseUi], Optional[CvChangeData]], None]
            :return: Registered handler function.
            :rtype: Callable[[Optional[CvAllData], Optional[BaseUi], Optional[CvChangeData]], None]
            """
            self.__events.append(CvHandler(event, function, class_name))
            return function

        return decorator

    def call(self, event: Type[CvEvent], changed_data: CvChangeData, *args):
        """Call every handler matching the event and class filter.

        :param event: Event type to dispatch.
        :type event: Type[CvEvent]
        :param changed_data: Event payload with current and previous box data.
        :type changed_data: CvChangeData
        :param args: Additional context forwarded to handlers.
        """
        for handler in self.__events:
            if handler.event is event and (handler.class_name is None
                                           or changed_data.box.class_name == handler.class_name):
                function_args = _form_args(handler.function, changed_data, *args)
                handler.function(**function_args)
