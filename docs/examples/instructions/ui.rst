UI Algorithm
============

Use the UI algorithm to run window and mouse instructions in sequence.

.. code-block:: python

   from apparser import App
   from apparser.geometry import Point, RelativelyPoint, Size
   from apparser.instructions import MouseClickTo, WindowMove, WindowResize, WriteText
   from apparser.instructions.algorithms import Algorithm

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = Algorithm([
           WindowMove(Point(50, 50)),
           WindowResize(Size(900, 700)),
           MouseClickTo(RelativelyPoint(0.5, 0.5)),
           WriteText("UI algorithm"),
       ])

   algorithm.perform(app.ui)

   app.stop_app()
