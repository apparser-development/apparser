from apparser.core import BaseUi
from apparser.instructions.ui.base import UiInstruction


class WindowToBackground(UiInstruction):
    @property
    def id(self) -> int:
        return 11

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_background()


class WindowToForeground(UiInstruction):
    @property
    def id(self) -> int:
        return 10

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
