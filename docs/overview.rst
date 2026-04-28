Overview
========

``apparser`` is a Python library for testing and managing computer programs.

Install
=======

.. code-block:: bash

   pip install apparser

Optional features
=================

.. code-block:: bash

   pip install "apparser[cv]"
   pip install "apparser[ocr]"
   pip install "apparser[speak]"
   pip install "apparser[all]"

Package map
===========

``apparser.core``
   Application and UI abstractions.

``apparser.geometry``
   Points, sizes, distances and relative coordinates.

``apparser.instructions``
   Executable actions, grouped instructions and lookup utilities.

``apparser.key_codes``
   Keyboard and mouse key abstractions.

``apparser.movers``
   Mouse movement strategies.

``apparser.text_readers``
   OCR and text extraction backends.

``apparser.speakers``
   Speech synthesis backends.

``apparser.cv``
   Computer vision readers, events, handlers and processes.

``apparser.debuggers`` and ``apparser.exceptions``
   Debugging helpers and library exceptions.
