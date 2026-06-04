from __future__ import annotations

from typing import Any

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.instructions.base import BaseInstruction


class FakeInstruction(BaseInstruction):
    def __init__(
        self,
        instruction_id: int = 1,
        raised_exception: Exception | None = None,
    ) -> None:
        self.instruction_id = instruction_id
        self.raised_exception = raised_exception
        self.calls: list[dict[str, Any]] = []

    @property
    def id(self) -> int:
        return self.instruction_id

    def perform(self, *args: Any, **kwargs: Any) -> None:
        self.calls.append({"args": args, "kwargs": kwargs})
        if self.raised_exception is not None:
            raise self.raised_exception
