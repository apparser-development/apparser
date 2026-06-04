from tests.utils.fakes.instructions.fake_debugger import FakeDebugger
from tests.utils.fakes.instructions.fake_instruction import FakeInstruction
from tests.utils.fakes.instructions.fake_int_attribute_instruction import (
    FakeIntAttributeInstruction,
)
from tests.utils.fakes.instructions.fake_ocr_instruction import FakeOcrInstruction
from tests.utils.fakes.instructions.fake_speak_instruction import FakeSpeakInstruction
from tests.utils.fakes.instructions.fake_str_attribute_instruction import (
    FakeStrAttributeInstruction,
)
from tests.utils.fakes.instructions.instruction_factory import make_instruction_type

__all__ = [
    "FakeDebugger",
    "FakeInstruction",
    "FakeIntAttributeInstruction",
    "FakeOcrInstruction",
    "FakeSpeakInstruction",
    "FakeStrAttributeInstruction",
    "make_instruction_type",
]
