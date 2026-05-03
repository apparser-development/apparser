Computer Vision
===============

Install the CV extra before using YOLO-based readers.

.. code-block:: bash

   pip install "apparser[cv]"

Track objects in a window and react to detected events.

.. code-block:: python

   import threading
   import time

   from apparser import App
   from apparser.cv import DefaultCvProcess, DefaultHandlers, YoloReader
   from apparser.cv.events import Detected, Moved
   from apparser.cv.models import CvChangeData
   from apparser.geometry import Size

   app = App("notepad.exe", "Notepad")

   reader = YoloReader("best.pt", persist=True, conf=0.5)
   handlers = DefaultHandlers()


   @handlers.register_handler(Detected, class_name="button")
   def on_detected(data: CvChangeData):
       print(data.box.class_name, data.box.track_id, data.box.x, data.box.y)


   @handlers.register_handler(Moved, class_name="button")
   def on_moved(data: CvChangeData):
       print("moved", data.box.track_id)


   process = DefaultCvProcess(reader, sleep_seconds=0.2)
   process.include_handlers(handlers)

   process.start(app.ui)
