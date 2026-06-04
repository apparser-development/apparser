import abc

from apparser.core import BaseUi

from apparser.instructions.ui.base import UiInstruction


class BaseAlgorithm(UiInstruction):
    """Define the base contract for instruction algorithms."""

    @property
    @abc.abstractmethod
    def id(self):
        """Return the unique algorithm identifier.

        :return: Algorithm identifier.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def add_instruction(self, instruction):
        """Add an instruction to the algorithm sequence.

        :param instruction: Instruction to append.
        """
        pass

    @property
    @abc.abstractmethod
    def instructions(self):
        """Return the configured instructions.

        :return: Instructions managed by the algorithm.
        """
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, *args, **kwargs):
        """Execute the algorithm for the provided UI context.

        :param ui: UI instance used during execution.
        :type ui: BaseUi
        :param args: Additional positional arguments for the execution flow.
        :param kwargs: Additional keyword arguments for the execution flow.
        """
        pass
