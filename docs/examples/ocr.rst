Text Recognition
==================

.. code-block:: python

   from apparser import App
   from apparser.geometry import Point, RelativelyPoint, Size
   from apparser.instructions import OCRAlgorithm

   algorithm = OCRAlgorithm([

   ])

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm.perform(app.ui)

   app.stop_app()
Result:
