import abc

from apparser.core import BaseUi
from apparser.cv.handlers import CvHandlers


class CvProcess(abc.ABC):
    """Define the interface for computer vision processing loops."""

    @abc.abstractmethod
    def start(self, ui: BaseUi):
        """Start processing computer vision data for a UI context.

        :param ui: UI instance used as the capture source.
        :type ui: BaseUi
        """
        pass

    @abc.abstractmethod
    def stop(self):
        """Stop the processing loop."""
        pass

    @abc.abstractmethod
    def include_handlers(self, handler: CvHandlers):
        """Add a handler registry to the processing loop.

        :param handler: Handler registry to include.
        :type handler: CvHandlers
        """
        pass
