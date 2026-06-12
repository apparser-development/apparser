from typing import Any

from tests.utils.external_stubs import install_external_stubs
from tests.utils.fakes.instructions.fake_instruction import FakeInstruction


install_external_stubs()

from apparser.core.ui.base import BaseUi
from apparser.text_readers import BaseTextReader


class FakeOcrInstruction(FakeInstruction):
    def perform(
        self,
        ui: BaseUi,
        text_reader: BaseTextReader,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().perform(ui, text_reader, *args, **kwargs)
