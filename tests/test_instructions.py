from appwindows import get_finder
from PIL import Image

from apparser.core import Ui

from apparser.cv.handlers import DefaultHandlers
from apparser.cv.events import Detected
from apparser.cv.models import CvAllData, CvClassData, CvHandler

handlers = DefaultHandlers()

@handlers.register_handler(Detected)
def detected_handler(all_data: CvAllData):
    print(all_data.some)

window = get_finder().get_window_by_title("apparser")

handlers.call(Detected, CvAllData("se", "some2"))
