Speak Algorithm
===============

Install the speech extra before using the speak algorithm.

.. code-block:: bash

   pip install "apparser[speak]"

Run speech instructions with a shared speaker backend.

.. code-block:: python

   from apparser import App
   from apparser.geometry import Size
   from apparser.instructions.algorithms import SpeakAlgorithm
   from apparser.instructions.speak import PlayTextAudio
   from apparser.speakers import ChatTTSSpeaker

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = SpeakAlgorithm(
       [PlayTextAudio("Automation started")],
       speaker=ChatTTSSpeaker(),
       debugger=None,
   )

   algorithm.perform(app.ui)
   app.stop_app()
