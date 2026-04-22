"""Tests for ui instructions."""

import pytest
from appwindows.geometry import Point, Size

import apparser.instructions.default.click as click_module
import apparser.instructions.default.press as press_module
import apparser.instructions.default.sleep as sleep_module
import apparser.instructions.default.write_text as write_text_module
from apparser.geometry import RelativelyPoint
from apparser.instructions.default.click import MouseClick, MouseClickTo
from apparser.instructions.default.mouse_move import MouseMove
from apparser.instructions.default.move_window import WindowMove
from apparser.instructions.default.press import PressKey, PressKeysCombination
from apparser.instructions.default.resize_window import WindowResize
from apparser.instructions.default.sleep import Sleep
from apparser.instructions.default.to_window import WindowToBackground, WindowToForeground
from apparser.instructions.default.write_text import WriteText
from apparser.key_codes import LeftClick, RightClick
from apparser.movers.base import BaseMover
from tests.utils.ui import InteractionUi


class DummyMover(BaseMover):
    def __init__(self):
        self.points = []

    def move(self, position: Point):
        self.points.append(position)


@pytest.mark.parametrize(
    ("instruction", "expected_id", "expected_name"),
    [
        (MouseClick(), 21, "MouseClick"),
        (MouseClickTo(Point(1, 2)), 22, "MouseClickTo"),
        (MouseMove(Point(1, 2), DummyMover()), 20, "MouseMove"),
        (WindowMove(Point(1, 2)), 12, "WindowMove"),
        (PressKey("a"), 30, "PressKey"),
        (PressKeysCombination(["a", "b"]), 31, "PressKeysCombination"),
        (WindowResize(Size(1, 2)), 13, "WindowResize"),
        (Sleep(1), 40, "Sleep"),
        (WindowToBackground(), 11, "WindowToBackground"),
        (WindowToForeground(), 10, "WindowToForeground"),
        (WriteText("text"), 32, "WriteText"),
    ],
)
def test_default_instruction_ids_and_names(instruction, expected_id, expected_name):
    assert instruction.id == expected_id
    assert instruction.name == expected_name


def test_mouse_click_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(click_module.mouse, "click", lambda: calls.append("left"))
    monkeypatch.setattr(click_module.mouse, "right_click", lambda: calls.append("right"))

    MouseClick().perform()
    MouseClick(RightClick()).perform()

    with pytest.raises(TypeError, match="click_type must be RightClick or LeftClick"):
        MouseClick("click")

    assert calls == ["left", "right"]


def test_mouse_click_to_validation_and_perform(monkeypatch):
    ui = InteractionUi()
    mover = DummyMover()
    clicks = []
    monkeypatch.setattr(click_module.mouse, "click", lambda: clicks.append("clicked"))

    instruction = MouseClickTo(Point(3, 4), LeftClick(), mover)
    instruction.perform(ui)

    with pytest.raises(ValueError, match="coordinates must be Point or RelativelyPoint"):
        MouseClickTo("coordinates")

    assert mover.points == [Point(3, 4)]
    assert clicks == ["clicked"]


def test_mouse_move_validation_and_perform():
    mover = DummyMover()
    ui = InteractionUi()

    with pytest.raises(TypeError, match="coordinates must be Point or RelativelyPoint"):
        MouseMove("coordinates", mover)

    with pytest.raises(TypeError, match="mover must be Mover"):
        MouseMove(Point(1, 2), "mover")

    instruction = MouseMove(RelativelyPoint(0.1, 0.2), mover)
    instruction.perform(ui)

    assert ui.global_calls == [instruction._MouseMove__coordinates]
    assert mover.points == [Point(9, 8)]


def test_move_window_validation_and_perform():
    ui = InteractionUi()

    with pytest.raises(TypeError, match="position must be of type Point"):
        WindowMove("position")

    instruction = WindowMove(Point(5, 6))
    instruction.perform(ui)

    assert ui.window.calls == [("move", Point(5, 6))]


def test_press_key_and_combination(monkeypatch):
    send_calls = []
    press_calls = []
    release_calls = []
    monkeypatch.setattr(press_module.keyboard, "send", lambda key: send_calls.append(key))
    monkeypatch.setattr(press_module.keyboard, "press", lambda key: press_calls.append(key))
    monkeypatch.setattr(
        press_module.keyboard,
        "release",
        lambda key: release_calls.append(key),
    )

    PressKey("a").perform()
    PressKey(RightClick()).perform()
    PressKeysCombination(["ctrl", "c"]).perform()

    with pytest.raises(TypeError, match="key_code must be KeyCode or str"):
        PressKey(1)

    with pytest.raises(TypeError, match="key_code must be KeyCode or str"):
        PressKeysCombination(["ctrl", 1]).perform()

    assert send_calls == ["a", "RIGHT"]
    assert press_calls == ["ctrl", "c", "ctrl"]
    assert release_calls == ["ctrl", "c"]


def test_resize_window_validation_and_perform():
    ui = InteractionUi()

    with pytest.raises(TypeError, match="size must be of type Size"):
        WindowResize("size")

    instruction = WindowResize(Size(20, 30))
    instruction.perform(ui)

    assert ui.window.calls == [("resize", Size(20, 30))]


def test_sleep_validation_and_perform(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr(sleep_module.time, "sleep", lambda seconds: sleep_calls.append(seconds))

    with pytest.raises(ValueError, match="sleep_time must be >= 0"):
        Sleep(0)

    instruction = Sleep(0.5)
    instruction.perform()

    assert sleep_calls == [0.5]


def test_to_window_instructions():
    ui = InteractionUi()

    WindowToForeground().perform(ui)
    WindowToBackground().perform(ui)

    assert ui.window.calls == [("to_foreground",), ("to_background",)]


def test_write_text_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(
        write_text_module.keyboard,
        "write",
        lambda text, pause: calls.append((text, pause)),
    )

    with pytest.raises(TypeError, match="text must be a string"):
        WriteText(1)

    with pytest.raises(TypeError, match="pause_time must be a number"):
        WriteText("text", "0.1")

    with pytest.raises(ValueError, match="text cannot be empty"):
        WriteText("")

    WriteText("hello", 0.2).perform()

    assert calls == [("hello", 0.2)]
