from apparser.core import BaseUi
from apparser.instructions.default.base import Instruction


class WindowToBackground(Instruction):
    @property
    def id(self) -> int:
        return 11

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_background()


class WindowToForeground(Instruction):
    @property
    def id(self) -> int:
        return 10

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
