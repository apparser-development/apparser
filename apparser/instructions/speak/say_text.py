from apparser.speakers import BaseSpeaker

from apparser.instructions.default import SayAudio
from apparser.instructions.speak.base import SpeakInstruction


class SayTextAudio(SpeakInstruction):
    """Synthesize text and play it through the microphone target device."""

    def __init__(self,
                 text: str,
                 sample_rate: int | float | None = None,
                 **settings):
        """Initialize a microphone-targeted speech instruction.

        :param text: Text to synthesize and play.
        :type text: str
        :param sample_rate: Audio sample rate in hertz.
        :type sample_rate: int | float | None
        :param settings: Additional audio playback settings.
        :type settings: dict[str, object]
        :raises TypeError: If ``text`` or ``sample_rate`` has an invalid type.
        :raises ValueError: If ``text`` is empty.
        """
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if len(text) < 1:
            raise ValueError("text cannot be empty")

        if sample_rate is not None and not isinstance(sample_rate, (int, float)):
            raise TypeError("sample_rate must be a number or None")

        self.__text = text
        self.__sample_rate = sample_rate
        self.__settings = settings

    @property
    def id(self) -> int:
        return 3001

    def perform(self, speaker: BaseSpeaker, *args, **kwargs):
        audio, audio_sample_rate = speaker.speak(self.__text)
        SayAudio(
            audio=audio,
            sample_rate=(
                audio_sample_rate
                if self.__sample_rate is None
                else self.__sample_rate
            ),
            **self.__settings,
        ).perform(*args, **kwargs)
