import abc

from apparser.core import Ui
from apparser.cv.models import CvAllData


class CvReader(abc.ABC):
    @abc.abstractmethod
    def read(self, ui: Ui) -> CvAllData:
        pass