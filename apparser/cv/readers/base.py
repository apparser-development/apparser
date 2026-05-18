"""Base interfaces for computer vision data readers."""

import abc

from apparser.core import BaseUi
from apparser.cv.models import CvAllData


class CvReader(abc.ABC):
    """Define the interface for computer vision data readers."""

    @abc.abstractmethod
    def read(self, ui: BaseUi) -> CvAllData:
        """Read computer vision data from a UI context.

        :param ui: UI instance used as the screenshot source.
        :type ui: BaseUi
        :return: Parsed computer vision data.
        :rtype: CvAllData
        """
        pass
