from __future__ import annotations

from typing import Any, TYPE_CHECKING

from tests.utils.stubs.ml.fake_torch_model import FakeTorchModel

if TYPE_CHECKING:
    from tests.utils.stubs.ml.torch_stub import TorchStub


class FakeTorchHub:
    def __init__(self, module: "TorchStub") -> None:
        self.module = module

    def load(self, **kwargs: Any) -> tuple[FakeTorchModel, None]:
        self.module.hub_load_calls.append(kwargs)
        return self.module.hub_model, None
