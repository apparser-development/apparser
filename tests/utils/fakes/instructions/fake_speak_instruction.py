from typing import Any

from tests.utils.external_stubs import install_external_stubs
from tests.utils.fakes.instructions.fake_instruction import FakeInstruction


install_external_stubs()

from apparser.core.ui.base import BaseUi
from apparser.speakers.base import BaseSpeaker


class FakeSpeakInstruction(FakeInstruction):
    def perform(
        self,
        speaker: BaseSpeaker,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().perform(speaker, *args, **kwargs)
