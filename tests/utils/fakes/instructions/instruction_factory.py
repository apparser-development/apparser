from __future__ import annotations

from typing import Any

from tests.utils.external_stubs import install_external_stubs


install_external_stubs()

from apparser.instructions.base import BaseInstruction


def make_instruction_type(name: str, instruction_id: int) -> type[BaseInstruction]:
    class GeneratedInstruction(BaseInstruction):
        @property
        def id(self) -> int:
            return instruction_id

        def perform(self, *args: Any, **kwargs: Any) -> None:
            return None

    GeneratedInstruction.__name__ = name
    return GeneratedInstruction
