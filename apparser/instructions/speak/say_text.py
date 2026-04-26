from apparser.core import BaseUi
from apparser.instructions.default import SayAudio
from apparser.speakers import BaseSpeaker

from apparser.instructions.speak.base import SpeakInstruction


class SayTextAudio(SpeakInstruction):
    """Synthesize text and play it through the microphone target device."""

    def __init__(self,
                 text: str,
                 sample_rate: int | float = 48000,
                 **settings):
        """Initialize a microphone-targeted speech instruction.

        :param text: Text to synthesize and play.
        :type text: str
        :param sample_rate: Audio sample rate in hertz.
        :type sample_rate: int | float
        :param settings: Additional audio playback settings.
        :type settings: dict[str, object]
        :raises TypeError: If ``text`` has an invalid type.
        :raises ValueError: If ``text`` is empty.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if len(text) < 1:
            raise ValueError("text cannot be empty")

        self.__text = text
        self.__sample_rate = sample_rate
        self.__settings = settings

    @property
    def id(self) -> int:
        return 301

    def perform(self, ui: BaseUi, speaker: BaseSpeaker, *args, **kwargs):
        audio = speaker.speak(self.__text)
        SayAudio(
            audio=audio,
            sample_rate=self.__sample_rate,
            **self.__settings,
        ).perform(*args, **kwargs)
