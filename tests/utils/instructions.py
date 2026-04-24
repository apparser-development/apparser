import sys
import types

import numpy


def _install_optional_dependency_stubs():
    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.device = lambda value: value

        class _Hub:
            @staticmethod
            def load(**kwargs):
                class _Model:
                    def to(self, device):
                        self.device = device

                    def apply_tts(self, **settings):
                        class _Audio:
                            def detach(self):
                                return self

                            def cpu(self):
                                return self

                            def numpy(self):
                                return numpy.array([], dtype=numpy.float32)

                        return _Audio()

                return _Model(), None

        torch.hub = _Hub()
        sys.modules["torch"] = torch

    if "ChatTTS" not in sys.modules:
        chattts = types.ModuleType("ChatTTS")

        class _Chat:
            class InferCodeParams:
                def __init__(self, spk_emb=None):
                    self.spk_emb = spk_emb

            def load(self, **kwargs):
                pass

            def sample_random_speaker(self):
                return "speaker"

            def infer(self, text, params_infer_code=None, **kwargs):
                return [numpy.array([], dtype=numpy.float32)]

        chattts.Chat = _Chat
        sys.modules["ChatTTS"] = chattts


_install_optional_dependency_stubs()

from apparser.instructions.ocr.base import OCRInstruction
from apparser.instructions.ui.base import UiInstruction


class DummyInstruction(UiInstruction):
    def __init__(
        self,
        calls=None,
        label: str = "instruction",
        instruction_id: int = 0,
        error: Exception | None = None,
    ):
        self.calls = [] if calls is None else calls
        self.label = label
        self.instruction_id = instruction_id
        self.error = error

    @property
    def id(self) -> int:
        return self.instruction_id

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def perform(self, ui, *args, **kwargs):
        if self.error is not None:
            raise self.error

        self.calls.append((self.label, ui, args, kwargs))


class DummyAiInstruction(OCRInstruction):
    def __init__(
        self,
        calls=None,
        label: str = "ai_instruction",
        instruction_id: int = 1,
        error: Exception | None = None,
    ):
        self.calls = [] if calls is None else calls
        self.label = label
        self.instruction_id = instruction_id
        self.error = error

    @property
    def id(self) -> int:
        return self.instruction_id

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def perform(self, ui, ai, *args, **kwargs):
        if self.error is not None:
            raise self.error

        self.calls.append((self.label, ui, ai, args, kwargs))
