Instructions Info
=======================

In ``apparser.instructions``, every concrete instruction inherits from
``BaseInstruction`` and must define the ``id`` property. This numeric
identifier is used for instruction lookup by number and for scenarios where an
instruction is described as ``(instruction_id, instruction_args)``.

How id lookup works
-----------------------

* The base contract is defined in
  ``apparser.instructions.base.BaseInstruction``: the ``id`` property is
  required and must return an ``int``.
* ``get_instruction_by_id()`` accepts only an integer and requires
  ``instruction_id >= 0``.
* Lookup is performed by exact ``id`` match without creating an instruction
  instance.
* If no match is found, ``InstructionWithIdNotFoundException`` is raised.
* ``id`` uniqueness is not validated separately. Based on the current
  implementation, if duplicates appear, the first matching class will be
  returned.

Lookup is performed through ``get_all_instructions()``, which scans the
``default``, ``ocr``, ``speak``, and ``ui`` packages and keeps only concrete,
non-abstract instruction classes.

.. important::

   Algorithm instructions currently not included in
   ``get_instruction_by_id()``.

Current numbering layout
------------------------

In the current codebase, identifiers are effectively grouped as follows:

* ``1-999`` - base instructions from ``apparser.instructions.default``
* ``1000-1499`` - UI instructions from ``apparser.instructions.ui``
* ``1500-1999`` - algorithms from ``apparser.instructions.ui.algorithms``
* ``2000-2999`` - OCR instructions from ``apparser.instructions.ocr``
* ``3000-3999`` - speech instructions from ``apparser.instructions.speak``

Numbering does not need to be continuous: the code only requires a non-negative
``id`` and no conflicts between classes that should be resolved by numeric
identifier.

Instructions available through get_instruction_by_id()
----------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - ``id``
     - Class
     - Purpose
   * - ``1``
     - ``MouseClick``
     - Perform a mouse click
   * - ``2``
     - ``PressKey``
     - Press a single key
   * - ``3``
     - ``PressKeysCombination``
     - Press a key combination
   * - ``4``
     - ``WriteText``
     - Type text from the keyboard
   * - ``5``
     - ``PlayAudio``
     - Play audio through an output device
   * - ``6``
     - ``SayAudio``
     - Play audio through a device used as a microphone target
   * - ``7``
     - ``PlayAudioFile``
     - Play an audio file
   * - ``8``
     - ``SayAudioFile``
     - Play an audio file through a device used as a microphone target
   * - ``9``
     - ``Sleep``
     - Pause execution for a fixed amount of time
   * - ``10``
     - ``PressKeyDown``
     - Press a single key down
   * - ``11``
     - ``PressKeyUp``
     - Release a single key
   * - ``12``
     - ``MouseUp``
     - Release a mouse button
   * - ``13``
     - ``MouseDown``
     - Press a mouse button down
   * - ``1000``
     - ``WindowToForeground``
     - Bring the window to the foreground
   * - ``1001``
     - ``WindowToBackground``
     - Send the window to the background
   * - ``1002``
     - ``WindowMove``
     - Move the window
   * - ``1003``
     - ``WindowResize``
     - Resize the window
   * - ``1004``
     - ``MouseMove``
     - Move the mouse cursor
   * - ``1005``
     - ``MouseClickTo``
     - Move the cursor to a point and click
   * - ``2000``
     - ``GetText``
     - Read text from a screen region
   * - ``2001``
     - ``MoveToText``
     - Move the cursor to matched text
   * - ``2002``
     - ``ClickOnText``
     - Find text and click it
   * - ``2003``
     - ``PrintAllText``
     - Print all detected text blocks
   * - ``2004``
     - ``PlotAllText``
     - Draw detected text on top of a screenshot
   * - ``2005``
     - ``WaitText``
     - Wait until matching text appears
   * - ``3000``
     - ``PlayTextAudio``
     - Synthesize text and play it as regular audio
   * - ``3001``
     - ``SayTextAudio``
     - Synthesize text and play it through a device used as a microphone
       target

Classes with their own id but not resolved by get_instruction_by_id()
------------------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - ``id``
     - Class
     - Purpose
   * - ``1500``
     - ``Algorithm``
     - Sequentially execute regular and UI instructions
   * - ``1501``
     - ``IdsAlgorithm``
     - Execute instructions described by numeric ``id`` values and arguments
   * - ``1502``
     - ``NamesAlgorithm``
     - Execute instructions described by class names and arguments
   * - ``1503``
     - ``OCRAlgorithm``
     - Execute instructions with a provided ``text_reader``
   * - ``1504``
     - ``SpeakAlgorithm``
     - Execute instructions with a provided ``speaker``
   * - ``1505``
     - ``UniqueAlgorithm``
     - Inject dependencies into instructions by argument type
