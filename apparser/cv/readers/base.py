import abc

import numpy as np

from apparser.cv.models import CvAllData


class CvReader(abc.ABC):
    @abc.abstractmethod
    def read(self, image: np.ndarray) -> CvAllData:
        pass