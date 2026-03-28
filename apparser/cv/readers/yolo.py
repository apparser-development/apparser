import numpy as np

from apparser.cv.models import CvAllData
from apparser.cv.readers.base import CvReader


class YoloReader(CvReader):
    def read(self, image: np.ndarray) -> CvAllData:
        pass
