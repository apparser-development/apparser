from __future__ import annotations

from typing import Any

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.instructions.base import BaseInstruction
from apparser.instructions.debuggers.base import BaseDebugger


class FakeDebugger(BaseDebugger):
    def __init__(self, call_inner: bool = True) -> None:
        self.call_inner = call_inner
        self.clear_calls = 0
        self.try_calls: list[dict[str, Any]] = []

    def clear_context(self) -> None:
        self.clear_calls += 1

    def try_perform(
        self,
        instruction: BaseInstruction,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.try_calls.append(
            {
                "instruction": instruction,
                "args": args,
                "kwargs": kwargs,
            }
        )
        if self.call_inner:
            instruction.perform(*args, **kwargs)
