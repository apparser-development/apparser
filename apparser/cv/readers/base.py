import abc

from apparser.core import BaseUi
from apparser.cv.models import CvAllData


class CvReader(abc.ABC):
    @abc.abstractmethod
    def read(self, ui: BaseUi) -> CvAllData:
        pass