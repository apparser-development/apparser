AI Algorithm
============

Install the optional OCR and speech dependencies before using the AI algorithm.

.. code-block:: bash

   pip install "apparser[ocr]" "apparser[speak]"

Combine UI, OCR and speech instructions in a single pipeline.

.. code-block:: python

   from apparser import App
   from apparser.geometry import RelativelyPoint, Size
   from apparser.instructions import MouseClickTo, Sleep, WriteText, AiAlgorithm
   from apparser.instructions.ocr import ClickOnText
   from apparser.instructions.speak import PlayTextAudio
   from apparser.speakers import ChatTTSSpeaker
   from apparser.text_readers import EasyOcrReader, ScreensController

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = AiAlgorithm([
           Sleep(1),
           MouseClickTo(RelativelyPoint(0.5, 0.5)),
           WriteText("apparser"),
           ClickOnText("File"),
           PlayTextAudio("Automation finished"),
       ],
       speaker=ChatTTSSpeaker(),
       text_reader=ScreensController(EasyOcrReader(["en"]))
   )

   algorithm.perform(app.ui)
   app.stop_app()
