import importlib

import numpy

from apparser.instructions.base import BaseInstruction


class PlayAudio(BaseInstruction):
    def __init__(self,
                 audio: numpy.ndarray | list,
                 sample_rate: int | float = 48000,
                 device: int | str | None = None,
                 blocking: bool = True,
                 **settings):
        if not isinstance(sample_rate, (int, float)):
            raise TypeError("sample_rate must be a number")

        if sample_rate <= 0:
            raise ValueError("sample_rate must be > 0")

        if not isinstance(blocking, bool):
            raise TypeError("blocking must be bool")

        if device is not None and not isinstance(device, (int, str)):
            raise TypeError("device must be int, str or None")

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
        self.__device = device
        self.__blocking = blocking
        self.__settings = settings

    @property
    def id(self) -> int:
        return 33

    def perform(self, *args, **kwargs):
        settings = {**self.__settings, **kwargs}
        samplerate = settings.pop("samplerate", self.__sample_rate)
        device = settings.pop("device", self.__device)
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
