import abc

from apparser.core import BaseUi
from apparser.text_readers import BaseTextReader
from apparser.instructions.base import BaseInstruction


class OCRInstruction(BaseInstruction):
    """Define the common interface for OCR-based instructions."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """Return the unique OCR instruction identifier.

        :return: OCR instruction identifier.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, text_reader: BaseTextReader, *args, **kwargs) -> BaseUi:
        """Execute the instruction with a text reader.

        :param ui: UI instance used during execution.
        :type ui: BaseUi
        :param text_reader: Text reader used to detect text.
        :type text_reader: BaseTextReader
        :param args: Additional positional arguments for the execution flow.
        :param kwargs: Additional keyword arguments for the execution flow.
        :return: Updated UI state when the implementation returns it.
        :rtype: BaseUi
        """
        pass
