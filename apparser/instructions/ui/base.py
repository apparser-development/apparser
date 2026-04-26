import abc

from apparser.core import BaseUi
from apparser.instructions.base import BaseInstruction


class UiInstruction(BaseInstruction):
    """Define the common interface for UI instructions."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """Return the unique UI instruction identifier.

        :return: UI instruction identifier.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, *args, **kwargs):
        """Execute the instruction for the provided UI context.

        :param ui: UI instance used during execution.
        :type ui: BaseUi
        :param args: Additional positional arguments for the execution flow.
        :param kwargs: Additional keyword arguments for the execution flow.
        """
        pass
