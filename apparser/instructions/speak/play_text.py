from apparser.core import BaseUi
from apparser.instructions.default import PlayAudio
from apparser.speakers import BaseSpeaker

from apparser.instructions.speak.base import SpeakInstruction


class PlayTextAudio(SpeakInstruction):
    def __init__(self,
                 text: str,
                 sample_rate: int | float = 48000,
                 **settings):
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if len(text) < 1:
            raise ValueError("text cannot be empty")

        self.__text = text
        self.__sample_rate = sample_rate
        self.__settings = settings

    @property
    def id(self) -> int:
        return 300

    def perform(self, ui: BaseUi, speaker: BaseSpeaker, *args, **kwargs):
        audio = speaker.speak(self.__text)
        PlayAudio(
            audio=audio,
            sample_rate=self.__sample_rate,
            **self.__settings,
        ).perform(*args, **kwargs)
