import abc


class BaseInstruction(abc.ABC):
    """Define the common interface for every instruction."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """Return the unique instruction identifier.

        :return: Instruction identifier.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def perform(self, *args, **kwargs):
        """Execute the instruction.

        :param args: Positional arguments required during execution.
        :param kwargs: Keyword arguments required during execution.
        """
        pass
