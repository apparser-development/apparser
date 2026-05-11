AI Algorithm
============

Install the optional OCR and speech dependencies before using the AI algorithm.

.. code-block:: bash

   pip install "apparser[all]"

Combine UI, OCR and speech instructions in a single pipeline.

.. code-block:: python

   from apparser import App
   from apparser.geometry import RelativelyPoint, Size

   from apparser.instructions.speak import PlayTextAudio
   from apparser.instructions.ocr import ClickOnText
   from apparser.instructions import MouseClickTo, Sleep, WriteText, UniqueAlgorithm

   from apparser.speakers import ChatTTSSpeaker
   from apparser.text_readers import EasyOcrReader, ScreensController

   app = App("notepad.exe", "Untitled - Notepad")

   algorithm = UniqueAlgorithm([
           Sleep(1),
           MouseClickTo(RelativelyPoint(0.5, 0.5)),
           WriteText("apparser"),
           ClickOnText("File"),
           PlayTextAudio("Automation finished"),
       ],
       attributes = [ChatTTSSpeaker(), ScreensController(EasyOcrReader(["en"]))]
   )

   algorithm.perform(app.ui)
   app.stop_app()
