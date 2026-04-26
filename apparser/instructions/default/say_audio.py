import importlib

import numpy

from apparser.instructions.base import BaseInstruction


class SayAudio(BaseInstruction):
    def __init__(self,
                 audio: numpy.ndarray | list,
                 sample_rate: int | float = 48000,
                 microphone_device: int | str | None = None,
                 blocking: bool = True,
                 **settings):
        if not isinstance(sample_rate, (int, float)):
            raise TypeError("sample_rate must be a number")

        if sample_rate <= 0:
            raise ValueError("sample_rate must be > 0")

        if not isinstance(blocking, bool):
            raise TypeError("blocking must be bool")

        if microphone_device is not None and not isinstance(microphone_device, (int, str)):
            raise TypeError("microphone_device must be int, str or None")

        audio = numpy.asarray(audio, dtype=numpy.float32)
        if audio.ndim not in [1, 2]:
            raise ValueError("audio must be 1D or 2D array")

        if audio.shape[0] <= 0:
            raise ValueError("audio cannot be empty")

        if audio.ndim == 2 and audio.shape[1] <= 0:
            raise ValueError("audio cannot be empty")

        self.__sounddevice = importlib.import_module("sounddevice")
        self.__audio = audio
        self.__sample_rate = sample_rate
        self.__microphone_device = microphone_device
        self.__blocking = blocking
        self.__settings = settings

    @property
    def id(self) -> int:
        return 6

    def perform(self, *args, **kwargs):
        settings = {**self.__settings, **kwargs}
        samplerate = settings.pop("samplerate", self.__sample_rate)
        device = settings.pop("microphone_device", self.__microphone_device)
        if device is None:
            device = settings.pop("device", None)
        if device is None:
            raise ValueError("microphone_device cannot be None")
        blocking = settings.pop("blocking", self.__blocking)
        mapping = settings.get("mapping")
        channels = 1
        if self.__audio.ndim == 2:
            channels = self.__audio.shape[1]
        if mapping is not None:
            channels = len(mapping)
        self.__sounddevice.check_output_settings(
            device=device,
            channels=channels,
            dtype=self.__audio.dtype.name,
            samplerate=samplerate,
        )
        self.__sounddevice.play(
            self.__audio,
            samplerate=samplerate,
            device=device,
            blocking=blocking,
            **settings,
        )
