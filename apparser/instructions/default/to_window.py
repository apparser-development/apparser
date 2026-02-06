from apparser import Ui
from apparser.instructions.default.base import Instruction


class ToBackgroundWindow(Instruction):
    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_background()


class ToForegroundWindow(Instruction):
    def perform(self, ui: Ui, *args, **kwargs):
        ui.window.to_foreground()
