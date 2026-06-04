from tests.utils.external_stubs import install_external_stubs
from tests.utils.fakes.instructions.fake_instruction import FakeInstruction


install_external_stubs()

from apparser.core.ui.base import BaseUi


class FakeStrAttributeInstruction(FakeInstruction):
    def perform(self, ui: BaseUi, name: str) -> None:
        super().perform(ui, name=name)
