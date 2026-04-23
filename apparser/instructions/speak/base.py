import abc

from apparser.core import BaseUi
from apparser.speakers import BaseSpeaker
from apparser.instructions.base import BaseInstruction


class SpeakInstruction(BaseInstruction):
    @property
    @abc.abstractmethod
    def id(self) -> int:
        pass

    @abc.abstractmethod
    def perform(self, ui: BaseUi, speaker: BaseSpeaker, *args, **kwargs) -> BaseUi:
        pass