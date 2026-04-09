import pytest
from appwindows.geometry import Point, Size

import apparser.instructions.default.click as click_module
import apparser.instructions.default.press as press_module
import apparser.instructions.default.sleep as sleep_module
import apparser.instructions.default.write_text as write_text_module
import apparser.movers.default as default_mover_module
from apparser.geometry import RelativelyPoint
from apparser.instructions.algorithms.default import Algorithm
from apparser.instructions.base import Instruction
from apparser.instructions.default.click import MouseClick, MouseClickTo
from apparser.instructions.default.mouse_move import MouseMove
from apparser.instructions.default.move_window import WindowMove
from apparser.instructions.default.press import PressKey, PressKeysCombination
from apparser.instructions.default.resize_window import WindowResize
from apparser.instructions.default.sleep import Sleep
from apparser.instructions.default.to_window import WindowToBackground, WindowToForeground
from apparser.instructions.default.write_text import WriteText
from apparser.key_codes import LeftClick, RightClick
from apparser.movers.base import Mover
from apparser.movers.default import DefaultMover


class FakeWindow:
    def __init__(self):
        self.calls = []

    def to_foreground(self):
        self.calls.append(('to_foreground',))

    def to_background(self):
        self.calls.append(('to_background',))

    def move(self, position):
        self.calls.append(('move', position))

    def resize(self, size):
        self.calls.append(('resize', size))


class FakeUi:
    def __init__(self):
        self.window = FakeWindow()
        self.global_calls = []

    def point_to_global(self, coordinates):
        self.global_calls.append(coordinates)
        if isinstance(coordinates, RelativelyPoint):
            return Point(9, 8)
        return coordinates


class DummyInstruction(Instruction):
    def __init__(self, calls, name):
        self.calls = calls
        self.name = name

    def perform(self, ui, *args, **kwargs):
        self.calls.append((self.name, ui, args, kwargs))


class DummyMover(Mover):
    def __init__(self):
        self.points = []

    def move(self, position: Point):
        self.points.append(position)


def test_algorithm_perform_and_add_instruction():
    calls = []
    ui = FakeUi()
    first = DummyInstruction(calls, 'first')
    second = DummyInstruction(calls, 'second')
    algorithm = Algorithm([first])

    algorithm.add_instruction(second)
    algorithm.perform(ui)

    assert algorithm.instructions == [first, second]
    assert ui.window.calls[0] == ('to_foreground',)
    assert [i[0] for i in calls] == ['first', 'second']


def test_algorithm_validation():
    algorithm = Algorithm([])

    with pytest.raises(TypeError, match='must be Instruction'):
        algorithm.add_instruction('instruction')

    with pytest.raises(TypeError, match='must be Instruction'):
        Algorithm(['instruction']).perform(FakeUi())


def test_mouse_click_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(click_module.mouse, 'click', lambda: calls.append('left'))
    monkeypatch.setattr(click_module.mouse, 'right_click', lambda: calls.append('right'))

    MouseClick().perform()
    MouseClick(RightClick()).perform()

    with pytest.raises(TypeError, match='click_type must be RightClick or LeftClick'):
        MouseClick('click')

    assert calls == ['left', 'right']


def test_mouse_click_to_validation_and_perform(monkeypatch):
    ui = FakeUi()
    mover = DummyMover()
    clicks = []
    monkeypatch.setattr(click_module.mouse, 'click', lambda: clicks.append('clicked'))

    instruction = MouseClickTo(Point(3, 4), LeftClick(), mover)
    instruction.perform(ui)

    with pytest.raises(ValueError, match='coordinates must be Point or RelativelyPoint'):
        MouseClickTo('coordinates')

    assert mover.points == [Point(3, 4)]
    assert clicks == ['clicked']


def test_mouse_move_validation_and_perform():
    mover = DummyMover()
    ui = FakeUi()

    with pytest.raises(TypeError, match='coordinates must be Point or RelativelyPoint'):
        MouseMove('coordinates', mover)

    with pytest.raises(TypeError, match='mover must be Mover'):
        MouseMove(Point(1, 2), 'mover')

    instruction = MouseMove(RelativelyPoint(0.1, 0.2), mover)
    instruction.perform(ui)

    assert ui.global_calls == [instruction._MouseMove__coordinates]
    assert mover.points == [Point(9, 8)]


def test_move_window_validation_and_perform():
    ui = FakeUi()

    with pytest.raises(TypeError, match='position must be of type Point'):
        WindowMove('position')

    instruction = WindowMove(Point(5, 6))
    instruction.perform(ui)

    assert ui.window.calls == [('move', Point(5, 6))]


def test_press_key_and_combination(monkeypatch):
    send_calls = []
    press_calls = []
    release_calls = []
    monkeypatch.setattr(press_module.keyboard, 'send', lambda key: send_calls.append(key))
    monkeypatch.setattr(press_module.keyboard, 'press', lambda key: press_calls.append(key))
    monkeypatch.setattr(press_module.keyboard, 'release', lambda key: release_calls.append(key))

    PressKey('a').perform()
    PressKey(RightClick()).perform()
    PressKeysCombination(['ctrl', 'c']).perform()

    with pytest.raises(TypeError, match='key_code must be KeyCode or str'):
        PressKey(1)

    with pytest.raises(TypeError, match='key_code must be KeyCode or str'):
        PressKeysCombination(['ctrl', 1]).perform()

    assert send_calls == ['a', 'RIGHT']
    assert press_calls == ['ctrl', 'c', 'ctrl']
    assert release_calls == ['ctrl', 'c']


def test_resize_window_validation_and_perform():
    ui = FakeUi()

    with pytest.raises(TypeError, match='size must be of type Size'):
        WindowResize('size')

    instruction = WindowResize(Size(20, 30))
    instruction.perform(ui)

    assert ui.window.calls == [('resize', Size(20, 30))]


def test_sleep_validation_and_perform(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr(sleep_module.time, 'sleep', lambda seconds: sleep_calls.append(seconds))

    with pytest.raises(ValueError, match='sleep_time must be >= 0'):
        Sleep(0)

    instruction = Sleep(0.5)
    instruction.perform()

    assert sleep_calls == [0.5]


def test_to_window_instructions():
    ui = FakeUi()

    WindowToForeground().perform(ui)
    WindowToBackground().perform(ui)

    assert ui.window.calls == [('to_foreground',), ('to_background',)]


def test_write_text_validation_and_perform(monkeypatch):
    calls = []
    monkeypatch.setattr(write_text_module.keyboard, 'write', lambda text, pause: calls.append((text, pause)))

    with pytest.raises(TypeError, match='text must be a string'):
        WriteText(1)

    with pytest.raises(TypeError, match='pause_time must be a number'):
        WriteText('text', '0.1')

    with pytest.raises(ValueError, match='text cannot be empty'):
        WriteText('')

    WriteText('hello', 0.2).perform()

    assert calls == [('hello', 0.2)]


def test_default_mover_validation_and_move(monkeypatch):
    calls = []
    monkeypatch.setattr(default_mover_module.mouse, 'move',
                        lambda x, y, absolute, duration: calls.append((x, y, absolute, duration)))

    with pytest.raises(TypeError, match='Duration must be a number'):
        DefaultMover('0')

    with pytest.raises(TypeError, match='Absolute must be a boolean'):
        DefaultMover(0, 'true')

    with pytest.raises(ValueError, match='Duration must be a >= 0'):
        DefaultMover(-1)

    mover = DefaultMover(0.5, False)
    mover.move(Point(7, 8))

    assert calls == [(7, 8, False, 0.5)]
