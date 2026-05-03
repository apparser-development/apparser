Quick Start
===========

Install the base package.

.. code-block:: bash

   pip install apparser

Open an application window and run a simple UI automation sequence.

.. code-block:: python

   from apparser import App
   from apparser.geometry import RelativelyPoint, Size
   from apparser.instructions import MouseClickTo, Sleep, WriteText
   from apparser.instructions.algorithms import Algorithm

   app = App(
       path_to_exe="notepad.exe",
       window_title="Untitled - Notepad",
       window_size=Size(900, 700),
       timeout=1.0,
   )

   algorithm = Algorithm(
       [
           Sleep(1),
           MouseClickTo(RelativelyPoint(0.5, 0.5)),
           WriteText("Hello from apparser"),
       ],
       debugger=None,
   )

   algorithm.perform(app.ui)
   app.stop_app()
