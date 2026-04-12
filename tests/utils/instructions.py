"""Reusable instruction doubles for tests."""

from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.default.base import Instruction


class DummyInstruction(Instruction):
    """Record perform calls for algorithm and debugger tests."""

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

    def perform(self, ui, *args, **kwargs):
        if self.error is not None:
            raise self.error

        self.calls.append((self.label, ui, args, kwargs))


class DummyAiInstruction(AiInstruction):
    """Record AI instruction calls for algorithm tests."""

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

    def perform(self, ui, ai, *args, **kwargs):
        if self.error is not None:
            raise self.error

        self.calls.append((self.label, ui, ai, args, kwargs))
