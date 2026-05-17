import abc

from apparser.core import BaseUi
from apparser.speakers import BaseSpeaker
from apparser.instructions.base import BaseInstruction


class SpeakInstruction(BaseInstruction):
    """Define the common interface for speech-based instructions."""

    @property
    @abc.abstractmethod
    def id(self) -> int:
        """Return the unique speech instruction identifier.

        :return: Speech instruction identifier.
        :rtype: int
        """
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, speaker: BaseSpeaker, *args, **kwargs) -> BaseUi:
        """Execute the instruction with a speaker backend.

        :param ui: UI instance used during execution.
        :type ui: BaseUi
        :param speaker: Speaker used to synthesize or play speech.
        :type speaker: BaseSpeaker
        :param args: Additional positional arguments for the execution flow.
        :param kwargs: Additional keyword arguments for the execution flow.
        :return: Updated UI state when the implementation returns it.
        :rtype: BaseUi
        """
        pass
