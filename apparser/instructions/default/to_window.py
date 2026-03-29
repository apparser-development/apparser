from apparser import WindowUi
from apparser.instructions.default.base import Instruction


class ToBackgroundWindow(Instruction):
    def perform(self, ui: WindowUi, *args, **kwargs):
        ui.window.to_background()


class ToForegroundWindow(Instruction):
    def perform(self, ui: WindowUi, *args, **kwargs):
        ui.window.to_foreground()
