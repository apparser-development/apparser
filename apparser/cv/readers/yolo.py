import numpy as np

from apparser.cv.models import CvData
from apparser.cv.readers.base import CvReader


class YoloReader(CvReader):
    def read(self, image: np.ndarray) -> CvData:
        pass 