from __future__ import annotations

from typing import Any

import numpy

from tests.utils.stubs.ml.infer_code_params import InferCodeParams


class ChatStub:
    InferCodeParams = InferCodeParams
    instances: list["ChatStub"] = []
    default_infer_result: list[numpy.ndarray] = []
    default_random_speaker = "random-speaker"

    def __init__(self) -> None:
        self.load_calls: list[dict[str, Any]] = []
        self.infer_calls: list[dict[str, Any]] = []
        self.sample_random_speaker_calls = 0
        self.__class__.instances.append(self)

    def load(self, **kwargs: Any) -> None:
        self.load_calls.append(kwargs)

    def sample_random_speaker(self) -> str:
        self.sample_random_speaker_calls += 1
        return self.default_random_speaker

    def infer(
        self,
        text: str,
        params_infer_code: Any = None,
        **settings: Any,
    ) -> list[numpy.ndarray]:
        self.infer_calls.append(
            {
                "text": text,
                "params_infer_code": params_infer_code,
                "settings": settings,
            }
        )
        return self.default_infer_result
