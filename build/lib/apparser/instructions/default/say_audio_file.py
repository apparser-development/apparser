import pathlib
import wave

import numpy

from apparser.instructions.base import BaseInstruction
from apparser.instructions.default.say_audio import SayAudio


class SayAudioFile(BaseInstruction):
    """Play voice audio loaded from a file."""

    def __init__(self,
                 path: str,
                 microphone_device: int | str | None = None,
                 blocking: bool = True,
                 **settings):
        """Initialize a file-based voice playback instruction.

        :param path: Path to the audio file.
        :type path: str
        :param microphone_device: Output device identifier for voice playback.
        :type microphone_device: int | str | None
        :param blocking: Whether playback should block execution.
        :type blocking: bool
        :param settings: Additional ``sounddevice.play`` settings.
        :type settings: dict[str, object]
        :raises TypeError: If ``path`` has an invalid type.
        :raises ValueError: If ``path`` is empty or the file does not exist.
        """
        if not isinstance(path, str):
            raise TypeError("path must be str")

        if len(path) <= 0:
            raise ValueError("path cannot be empty")

        self.__path = pathlib.Path(path)
        if not self.__path.is_file():
            raise ValueError("file does not exist")

        audio, sample_rate = self.__read_audio()
        self.__instruction = SayAudio(
            audio=audio,
            sample_rate=sample_rate,
            microphone_device=microphone_device,
            blocking=blocking,
            **settings,
        )

    def __read_audio(self) -> tuple[numpy.ndarray, int]:
        with wave.open(str(self.__path), "rb") as file:
            channels = file.getnchannels()
            sample_rate = file.getframerate()
            sample_width = file.getsampwidth()
            frames = file.getnframes()
            audio = file.readframes(frames)

        if sample_width == 1:
            audio = (numpy.frombuffer(audio, dtype=numpy.uint8).astype(numpy.float32) - 128) / 128
        elif sample_width == 2:
            audio = numpy.frombuffer(audio, dtype=numpy.int16).astype(numpy.float32) / 32768
        elif sample_width == 4:
            audio = numpy.frombuffer(audio, dtype=numpy.int32).astype(numpy.float32) / 2147483648
        else:
            raise ValueError("unsupported sample width")

        if channels > 1:
            audio = audio.reshape(-1, channels)

        return audio, sample_rate

    @property
    def id(self) -> int:
        return 8

    def perform(self, *args, **kwargs):
        self.__instruction.perform(*args, **kwargs)
