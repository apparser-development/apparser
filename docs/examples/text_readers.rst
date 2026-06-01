Text Readers
================

Install the OCR extra before using OCR readers.

.. code-block:: bash

   pip install "apparser[ocr]"

Read text directly from an image with EasyOCR.

.. code-block:: python

   import numpy
   from PIL import Image

   from apparser.text_readers import EasyOcrReader

   image = numpy.array(Image.open("screen.png"))
   reader = EasyOcrReader(["en"])

   texts = reader.read_image(image)
   for text in texts:
       print(text.text, text.coordinates)

Wrap a reader with grayscale preprocessing and screenshot caching.

.. code-block:: python

   import numpy
   from PIL import Image

   from apparser.text_readers import PaddleTextReader, ScreensController, WhiteBlackReader

   image = numpy.array(Image.open("screen.png"))
   reader = ScreensController(WhiteBlackReader(PaddleTextReader(lang="en")))

   first_result = reader.read_image(image)
   second_result = reader.read_image(image)

   print(len(first_result), len(second_result))
