from apparser.core import Ui
from apparser.instructions.default.base import Instruction


class WindowToBackground(Instruction):
    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_background()


class WindowToForeground(Instruction):
    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_foreground()
