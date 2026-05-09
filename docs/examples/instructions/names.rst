Names Algorithm
===============

Use the names algorithm when instructions are stored as class names with argument lists.

.. code-block:: python

   from apparser import App
   from apparser.geometry import RelativelyPoint, Size
   from apparser.instructions import NamesAlgorithm

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = NamesAlgorithm([
           ("Sleep", [1]),
           ("MouseClickTo", [RelativelyPoint(0.5, 0.5)]),
           ("WriteText", ["Hello from NamesAlgorithm"]),
   ])

   algorithm.perform(app.ui)
   app.stop_app()
