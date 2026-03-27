import abc

import numpy as np

from apparser.cv.models import CvData


class CvReader(abc.ABC):
    @abc.abstractmethod
    def read(self, image: np.ndarray) -> CvData:
        pass