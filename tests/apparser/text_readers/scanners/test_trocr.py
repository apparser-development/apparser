from __future__ import annotations

import sys
from types import ModuleType
from typing import Any

import numpy
import pytest

from apparser.text_readers.scanners import TrocrScanner


class PixelValuesStub:
    def __init__(self) -> None:
        self.device: str | None = None

    def to(self, device: str) -> "PixelValuesStub":
        self.device = device
        return self


class ProcessorResultStub:
    def __init__(self, pixel_values: PixelValuesStub) -> None:
        self.pixel_values = pixel_values


class ProcessorStub:
    instances: list["ProcessorStub"] = []

    def __init__(self, name: str) -> None:
        self.name = name
        self.pixel_values = PixelValuesStub()
        self.calls: list[dict[str, Any]] = []
        self.decode_calls: list[dict[str, Any]] = []
        self.__class__.instances.append(self)

    @classmethod
    def from_pretrained(cls, name: str) -> "ProcessorStub":
        return cls(name)

    def __call__(
        self,
        images: Any,
        return_tensors: str,
    ) -> ProcessorResultStub:
        self.calls.append(
            {
                "images": images,
                "return_tensors": return_tensors,
            }
        )
        return ProcessorResultStub(self.pixel_values)

    def batch_decode(
        self,
        generated_ids: list[int],
        skip_special_tokens: bool,
    ) -> list[str]:
        self.decode_calls.append(
            {
                "generated_ids": generated_ids,
                "skip_special_tokens": skip_special_tokens,
            }
        )
        return ["recognized text"]


class ModelStub:
    instances: list["ModelStub"] = []

    def __init__(self, name: str) -> None:
        self.name = name
        self.device: str | None = None
        self.generate_calls: list[PixelValuesStub] = []
        self.__class__.instances.append(self)

    @classmethod
    def from_pretrained(cls, name: str) -> "ModelStub":
        return cls(name)

    def to(self, device: str) -> None:
        self.device = device

    def generate(self, pixel_values: PixelValuesStub) -> list[int]:
        self.generate_calls.append(pixel_values)
        return [1, 2, 3]


class TransformersStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("transformers")
        ProcessorStub.instances = []
        ModelStub.instances = []
        self.TrOCRProcessor = ProcessorStub
        self.VisionEncoderDecoderModel = ModelStub


class CudaStub:
    def is_available(self) -> bool:
        return True


class TorchModuleStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("torch")
        self.cuda = CudaStub()


def test_trocr_scanner_reads_text(monkeypatch: pytest.MonkeyPatch) -> None:
    transformers_stub = TransformersStub()
    torch_stub = TorchModuleStub()
    monkeypatch.setitem(sys.modules, "transformers", transformers_stub)
    monkeypatch.setitem(sys.modules, "torch", torch_stub)
    scanner = TrocrScanner(
        model_name="model",
        processor_name="processor",
    )
    image = numpy.zeros((2, 2, 3), dtype=numpy.uint8)

    result = scanner.read_image(image)

    processor = ProcessorStub.instances[0]
    model = ModelStub.instances[0]
    assert processor.name == "processor"
    assert model.name == "model"
    assert model.device == "cuda"
    assert processor.pixel_values.device == "cuda"
    assert model.generate_calls == [processor.pixel_values]
    assert processor.decode_calls == [
        {
            "generated_ids": [1, 2, 3],
            "skip_special_tokens": True,
        }
    ]
    assert result == "recognized text"
