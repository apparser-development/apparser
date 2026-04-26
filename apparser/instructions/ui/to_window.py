from apparser.core import BaseUi
from apparser.instructions.ui.base import UiInstruction


class WindowToBackground(UiInstruction):
    @property
    def id(self) -> int:
        return 101

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_background()


class WindowToForeground(UiInstruction):
    @property
    def id(self) -> int:
        return 100

    def perform(self, ui: BaseUi, *args, **kwargs):
        ui.window.to_foreground()
