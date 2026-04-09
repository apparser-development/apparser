from apparser.core import Ui
from apparser.instructions.base import Instruction


class WindowToBackground(Instruction):
    @property
    def id(self) -> int:
        return 11

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_background()


class WindowToForeground(Instruction):
    @property
    def id(self) -> int:
        return 10

    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_foreground()
