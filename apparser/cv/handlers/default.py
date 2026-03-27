from typing import Callable, Type, Optional, Any
import inspect

from apparser.core import Ui
from apparser.cv.handlers.base import CvHandlers
from apparser.cv.events import CvEvent
from apparser.cv.models import CvAllData, CvHandler, CvClassData


def _form_args(function: Callable, *args) -> dict[str, Any]:
    result = {}
    function_signature = inspect.signature(function)
    for arg in function_signature.parameters.values():
        for kwarg in args:
            if arg.annotation is type(kwarg):
                result[arg.name] = kwarg
    return result


class DefaultHandlers(CvHandlers):
    def __init__(self):
        self.__events: list[CvHandler] = []

    def register_handler(self, event: Type[CvEvent]):
        if event is CvEvent:
            raise TypeError("event must be a apparser.cv.events.CvEvent")
        def decorator(function: Callable[[Optional[CvAllData], Optional[Ui], Optional[CvClassData]], None]):
            self.__events.append(CvHandler(event, function))
            return function
        return decorator

    def call(self, event: Type[CvEvent], *args):
        for handler in self.__events:
            if handler.event is event:
                function_args = _form_args(handler.function, *args)
                handler.function(**function_args)