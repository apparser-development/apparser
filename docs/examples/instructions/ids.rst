Ids Algorithm
=============

Use the ids algorithm when instructions are stored as numeric identifiers with argument lists.

.. code-block:: python

   from apparser import App
   from apparser.geometry import RelativelyPoint, Size
   from apparser.instructions.algorithms import IdsAlgorithm

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = IdsAlgorithm([
           (9, [1]),
           (105, [RelativelyPoint(0.5, 0.5)]),
           (4, ["Hello from IdsAlgorithm"]),
       ], debugger=None,
   )

   algorithm.perform(app.ui)
   app.stop_app()
