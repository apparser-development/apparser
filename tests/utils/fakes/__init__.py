from tests.utils.fakes.backends.fake_speaker import FakeSpeaker
from tests.utils.fakes.backends.fake_text_reader import FakeTextReader
from tests.utils.fakes.cv.fake_changes_checker import FakeChangesChecker
from tests.utils.fakes.cv.fake_cv_handlers import FakeCvHandlers
from tests.utils.fakes.cv.fake_cv_reader import FakeCvReader
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
from tests.utils.fakes.ui.fake_ui import FakeUi
from tests.utils.fakes.ui.fake_window import FakeWindow
from tests.utils.fakes.ui.fake_window_points import FakeWindowPoints

__all__ = [
    "FakeChangesChecker",
    "FakeCvHandlers",
    "FakeCvReader",
    "FakeDebugger",
    "FakeInstruction",
    "FakeIntAttributeInstruction",
    "FakeOcrInstruction",
    "FakeSpeaker",
    "FakeSpeakInstruction",
    "FakeStrAttributeInstruction",
    "FakeTextReader",
    "FakeUi",
    "FakeWindow",
    "FakeWindowPoints",
    "make_instruction_type",
]
