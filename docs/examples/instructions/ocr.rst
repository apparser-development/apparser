OCR Algorithm
=============

Install the OCR extra before using the OCR algorithm.

.. code-block:: bash

   pip install "apparser[ocr]"

Run OCR instructions with a shared text reader.

.. code-block:: python

   from apparser import App
   from apparser.geometry import Size
   from apparser.instructions import OCRAlgorithm
   from apparser.instructions.ocr import ClickOnText, PrintAllText
   from apparser.text_readers import EasyOcrReader, ScreensController, WhiteBlackReader

   app = App("notepad.exe", "Untitled - Notepad")

   reader = ScreensController(WhiteBlackReader(EasyOcrReader(["en"])))

   algorithm = OCRAlgorithm([
        PrintAllText(),
        ClickOnText("File")
       ],
       text_reader=reader
   )

   algorithm.perform(app.ui)
   app.stop_app()
