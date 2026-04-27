import importlib

import numpy

from apparser.speakers.base import BaseSpeaker


class TorchSpeaker(BaseSpeaker):
    """Generate speech by using a Torch-backed Silero model."""

    def __init__(self,
                 language: str = "ru",
                 speaker_model: str = "v5_ru",
                 speaker: str = "xenia",
                 sample_rate: int = 48000,
                 device: str | object = "cpu",
                 repo_or_dir: str = "snakers4/silero-models",
                 model: str = "silero_tts",
                 source: str = "github",
                 trust_repo: bool | str | None = None,
                 skip_validation: bool | None = None,
                 **settings):
        """Initialize a Torch speaker backend.

        :param language: Language code for the loaded model.
        :type language: str
        :param speaker_model: Speaker model identifier.
        :type speaker_model: str
        :param speaker: Speaker name used for synthesis.
        :type speaker: str
        :param sample_rate: Output sample rate.
        :type sample_rate: int
        :param device: Torch device used for inference.
        :type device: str | object
        :param repo_or_dir: Torch Hub repository or directory.
        :type repo_or_dir: str
        :param model: Torch Hub model name.
        :type model: str
        :param source: Torch Hub source.
        :type source: str
        :param trust_repo: Optional Torch Hub trust setting.
        :type trust_repo: bool | str | None
        :param skip_validation: Optional Torch Hub validation setting.
        :type skip_validation: bool | None
        :param settings: Additional Torch Hub load settings.
        :type settings: dict[str, object]
        """
        self.__speaker = speaker
        self.__sample_rate = sample_rate
        self.__torch = importlib.import_module("torch")
        hub_settings = {
            "repo_or_dir": repo_or_dir,
            "model": model,
            "language": language,
            "speaker": speaker_model,
            "source": source,
            **settings,
        }
        if trust_repo is not None:
            hub_settings["trust_repo"] = trust_repo
        if skip_validation is not None:
            hub_settings["skip_validation"] = skip_validation
        self.__model, _ = self.__torch.hub.load(**hub_settings)
        self.__device = device
        if isinstance(device, str):
            self.__device = self.__torch.device(device)
        self.__model.to(self.__device)

    def speak(self, text: str, **settings) -> numpy.ndarray:
        """Convert text into audio data.

        :param text: Text to synthesize.
        :type text: str
        :param settings: Additional synthesis settings.
        :type settings: dict[str, object]
        :return: Generated audio samples.
        :rtype: numpy.ndarray
        """
        audio = self.__model.apply_tts(
            text=text,
            speaker=self.__speaker,
            sample_rate=self.__sample_rate,
            **settings,
        )
        return audio.detach().cpu().numpy()
