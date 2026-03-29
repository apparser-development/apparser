from apparser import WindowUi

from apparser.cv.models import CvAllData
from apparser.cv.events import Detected
from apparser.cv import DefaultHandlers

handlers = DefaultHandlers()


@handlers.register_handler(Detected, class_name="SomeClass")
def detected_handler(all_data: CvAllData, ui: WindowUi):
    print(all_data.boxes[0].height)


@handlers.register_handler(Detected, class_name="SomeClass")
def detected_handler(all_data: CvAllData):
    print(all_data.boxes[0].height)


@handlers.register_handler(Detected, class_name="SomeClass")
def detected_handler(all_data: CvAllData):
    print(all_data.boxes[0].height)
