from apparser import DesktopUi
from apparser.instructions import MouseMove
from apparser.geometry import RelativelyPoint


ui = DesktopUi()

MouseMove(RelativelyPoint(0.5, 0.5)).perform(ui)
