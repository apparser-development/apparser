from __future__ import annotations

import numpy


class FakeTorchTensor:
    def __init__(self, values: list[float] | numpy.ndarray) -> None:
        self.values = numpy.asarray(values, dtype=numpy.float32)

    def detach(self) -> "FakeTorchTensor":
        return self

    def cpu(self) -> "FakeTorchTensor":
        return self

    def numpy(self) -> numpy.ndarray:
        return self.values
