import importlib

import numpy

from apparser.speakers.base import BaseSpeaker


class ChatTTSSpeaker(BaseSpeaker):
    """Generate speech by using ChatTTS."""

    def __init__(self,
                 speaker: str | None = None,
                 source: str = "local",
                 force_redownload: bool = False,
                 compile: bool = False,
                 custom_path: str | None = None,
                 device: str | object | None = None,
                 coef: str | None = None,
                 use_flash_attn: bool = False,
                 use_vllm: bool = False,
                 experimental: bool = False,
                 enable_cache: bool = True):
        """Initialize a ChatTTS speaker backend.

        :param speaker: Speaker embedding value used for synthesis.
        :type speaker: str | None
        :param source: Model source passed to ChatTTS.
        :type source: str
        :param force_redownload: Whether model files should be redownloaded.
        :type force_redownload: bool
        :param compile: Whether ChatTTS should compile its model.
        :type compile: bool
        :param custom_path: Custom model path.
        :type custom_path: str | None
        :param device: Device passed to ChatTTS.
        :type device: str | object | None
        :param coef: Additional ChatTTS coefficient setting.
        :type coef: str | None
        :param use_flash_attn: Whether flash attention should be enabled.
        :type use_flash_attn: bool
        :param use_vllm: Whether vLLM support should be enabled.
        :type use_vllm: bool
        :param experimental: Whether experimental mode should be enabled.
        :type experimental: bool
        :param enable_cache: Whether ChatTTS cache should be enabled.
        :type enable_cache: bool
        """
        self.__chattts = importlib.import_module("ChatTTS")
        self.__torch = importlib.import_module("torch")
        self.__chat = self.__chattts.Chat()
        if isinstance(device, str):
            device = self.__torch.device(device)
        self.__chat.load(
            source=source,
            force_redownload=force_redownload,
            compile=compile,
            custom_path=custom_path,
            device=device,
            coef=coef,
            use_flash_attn=use_flash_attn,
            use_vllm=use_vllm,
            experimental=experimental,
            enable_cache=enable_cache,
        )
        self.__speaker = speaker
        if self.__speaker is None:
            self.__speaker = self.__chat.sample_random_speaker()

    def speak(self, text: str, **settings) -> numpy.ndarray:
        """Convert text into audio data.

        :param text: Text to synthesize.
        :type text: str
        :param settings: Additional ChatTTS inference settings.
        :type settings: dict[str, object]
        :return: Generated audio samples.
        :rtype: numpy.ndarray
        """
        speaker = settings.pop("speaker", self.__speaker)
        params_infer_code = settings.pop("params_infer_code", None)
        if params_infer_code is None:
            params_infer_code = self.__chattts.Chat.InferCodeParams(
                spk_emb=speaker,
            )
        elif getattr(params_infer_code, "spk_emb", None) is None:
            params_infer_code.spk_emb = speaker
        audio = self.__chat.infer(
            text,
            params_infer_code=params_infer_code,
            **settings,
        )
        if len(audio) == 0:
            return numpy.array([], dtype=numpy.float32)
        if len(audio) == 1:
            return numpy.asarray(audio[0])
        return numpy.concatenate([numpy.asarray(i) for i in audio])
