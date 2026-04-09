from types import SimpleNamespace

import numpy
import pytest
from appwindows.geometry import Point

import apparser.instructions.ai.click_on_text as click_on_text_module
import apparser.instructions.ai.move_to_text as move_to_text_module
import apparser.instructions.ai.plot_text as plot_text_module
from apparser.exceptions import TextNotFoundException
from apparser.geometry import RelativelyPoint
from apparser.algorithms.ai import AiAlgorithm
from apparser.instructions.ai.base import AiInstruction
from apparser.instructions.ai.click_on_text import ClickOnText
from apparser.instructions.ai.move_to_text import MoveToText
from apparser.instructions.ai.plot_text import PlotAllText, _Painter
from apparser.instructions.ai.print_all_text import PrintAllText
from apparser.instructions.ai.text_getter import GetText
from apparser.instructions.base import Instruction
from apparser.text_readers.text_data import TextData


class FakeAiReader:
    def __init__(self, answer=None):
        self.answer = answer or []
        self.calls = []

    def read_image(self, image):
        self.calls.append(image)
        return self.answer


class FakeWindow:
    def __init__(self):
        self.calls = []

    def to_foreground(self):
        self.calls.append('foreground')


class FakeUi:
    def __init__(self, screenshot=None):
        self.window = FakeWindow()
        self.screenshot = screenshot
        self.global_calls = []
        self.local_calls = []

    def point_to_global(self, coordinates):
        self.global_calls.append(coordinates)
        if isinstance(coordinates, RelativelyPoint):
            return Point(2, 3)
        return coordinates

    def point_to_local(self, coordinates):
        self.local_calls.append(coordinates)
        return coordinates

    def get_screenshot(self):
        return self.screenshot


class DummyInstruction(Instruction):
    def __init__(self, calls, name):
        self.calls = calls
        self.name = name

    def perform(self, ui, *args, **kwargs):
        self.calls.append((self.name, ui, args, kwargs))


class DummyAiInstruction(AiInstruction):
    def __init__(self, calls, name):
        self.calls = calls
        self.name = name

    def perform(self, ui, ai):
        self.calls.append((self.name, ui, ai))


class FakeImage:
    def __init__(self, array):
        self.array = array
        self.crop_calls = []
        self.show_calls = 0

    def crop(self, box):
        self.crop_calls.append(box)
        return self

    def show(self):
        self.show_calls += 1

    def __array__(self, dtype=None, copy=None):
        return self.array


def test_ai_algorithm_perform_and_add_instruction():
    calls = []
    ui = FakeUi()
    ai_reader = FakeAiReader()
    first = DummyInstruction(calls, 'instruction')
    second = DummyAiInstruction(calls, 'ai_instruction')
    algorithm = AiAlgorithm([first], ai_reader=ai_reader)

    algorithm.add_instruction(second)
    algorithm.perform(ui)

    assert algorithm.instructions == [first, second]
    assert ui.window.calls == ['foreground']
    assert calls[0][0] == 'instruction'
    assert calls[1] == ('ai_instruction', ui, ai_reader)


def test_ai_algorithm_validation():
    algorithm = AiAlgorithm([], ai_reader=FakeAiReader())

    with pytest.raises(TypeError, match='must be Instruction or AiInstruction'):
        algorithm.add_instruction('instruction')

    with pytest.raises(TypeError, match='must be Instruction or AiInstruction'):
        AiAlgorithm(['instruction'], ai_reader=FakeAiReader()).perform(FakeUi())


def test_click_on_text_perform_order(monkeypatch):
    calls = []

    class FakeMoveToText:
        def __init__(self, *args, **kwargs):
            calls.append(('move_init', args, kwargs))

        def perform(self, ui, ai):
            calls.append(('move_perform', ui, ai))

    class FakeSleep:
        def __init__(self, sleep_time):
            calls.append(('sleep_init', sleep_time))

        def perform(self, ui, ai):
            calls.append(('sleep_perform', ui, ai))

    class FakeMouseClick:
        def __init__(self, click_type):
            calls.append(('click_init', click_type))

        def perform(self, ui, ai):
            calls.append(('click_perform', ui, ai))

    monkeypatch.setattr(click_on_text_module, 'MoveToText', FakeMoveToText)
    monkeypatch.setattr(click_on_text_module, 'Sleep', FakeSleep)
    monkeypatch.setattr(click_on_text_module, 'MouseClick', FakeMouseClick)

    ui = FakeUi()
    ai = FakeAiReader()
    ClickOnText('text', sleep_time_before_move=0.3).perform(ui, ai)

    assert calls[0][0] == 'move_init'
    assert calls[1] == ('sleep_init', 0.3)
    assert calls[2] == ('move_perform', ui, ai)
    assert calls[3] == ('sleep_perform', ui, ai)
    assert calls[4][0] == 'click_init'
    assert calls[5] == ('click_perform', ui, ai)


def test_move_to_text_find_text_and_property(monkeypatch):
    monkeypatch.setattr(move_to_text_module.fuzz, 'token_sort_ratio',
                        lambda needed, text: {'wrong': 10, 'best': 95}[text])
    instruction = MoveToText('needle')
    texts = [
        TextData('wrong', [Point(0, 0)]),
        TextData('best', [Point(1, 1)]),
    ]

    found, rating = instruction.find_text(texts)

    assert instruction.text == 'needle'
    assert found == texts[1]
    assert rating == 95


def test_move_to_text_perform_success(monkeypatch):
    move_calls = []
    getter = SimpleNamespace(
        global_answer=[
            TextData('target', [Point(0, 0), Point(10, 0), Point(10, 20), Point(0, 20)])
        ],
        perform=lambda ui, ai: None,
    )
    ui = FakeUi()

    class FakeMouseMove:
        def __init__(self, point):
            move_calls.append(('init', point))

        def perform(self, ui):
            move_calls.append(('perform', ui))

    monkeypatch.setattr(move_to_text_module.fuzz, 'token_sort_ratio', lambda needed, text: 100)
    monkeypatch.setattr(move_to_text_module, 'MouseMove', FakeMouseMove)

    instruction = MoveToText('target', min_similarity=0.9, offset=RelativelyPoint(0.5, 0.5), text_getter=getter)
    instruction.perform(ui, FakeAiReader())

    assert len(ui.global_calls) == 1
    assert isinstance(ui.global_calls[0], RelativelyPoint)
    assert ui.global_calls[0].x == 0.5
    assert ui.global_calls[0].y == 0.5
    assert ui.local_calls == [Point(2, 3)]
    assert move_calls == [('init', Point(7, 13)), ('perform', ui)]


def test_move_to_text_perform_raises_when_similarity_is_low(monkeypatch):
    getter = SimpleNamespace(
        global_answer=[TextData('target', [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])],
        perform=lambda ui, ai: None,
    )
    monkeypatch.setattr(move_to_text_module.fuzz, 'token_sort_ratio', lambda needed, text: 0)

    with pytest.raises(TextNotFoundException):
        MoveToText('target', min_similarity=1.0, text_getter=getter).perform(FakeUi(), FakeAiReader())


def test_painter_draws_coordinates_and_lines():
    calls = []
    draw = SimpleNamespace(
        rectangle=lambda shape, outline, width: calls.append(('rectangle', shape, outline, width)),
        text=lambda position, text, fill: calls.append(('text', position, text, fill)),
    )
    painter = _Painter(draw, (1, 2, 3, 4))
    data = [TextData('word', [Point(5, -20), Point(15, -20), Point(15, -5), Point(5, -5)])]

    painter.draw(data)

    assert calls == [
        ('text', (65, -15), 'word', (1, 2, 3, 4)),
        ('rectangle', [(5, -20), (15, -5)], (1, 2, 3, 4), 1),
    ]


def test_plot_all_text_perform(monkeypatch):
    draw_calls = []
    image = FakeImage(numpy.array([[1, 2], [3, 4]]))
    getter = SimpleNamespace(
        local_answer=[TextData('word', [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)])],
        screenshot=image,
        perform=lambda ui, ai: None,
    )

    class FakeDraw:
        def rectangle(self, shape, outline, width):
            draw_calls.append(('rectangle', shape, outline, width))

        def text(self, position, text, fill):
            draw_calls.append(('text', position, text, fill))

    monkeypatch.setattr(plot_text_module.ImageDraw, 'Draw', lambda screenshot: FakeDraw())

    PlotAllText(text_getter=getter, color_rgba=(1, 2, 3, 4)).perform(FakeUi(), FakeAiReader())

    assert draw_calls == [
        ('text', (60, 10), 'word', (1, 2, 3, 4)),
        ('rectangle', [(0, 0), (10, 10)], (1, 2, 3, 4), 1),
    ]
    assert image.show_calls == 1


def test_print_all_text_perform(monkeypatch):
    printed = []
    getter = SimpleNamespace(
        global_answer=[TextData('word', [Point(1, 2), Point(3, 4)])],
        perform=lambda ui, ai: None,
    )
    monkeypatch.setattr('builtins.print', lambda line: printed.append(line))

    PrintAllText(text_getter=getter).perform(FakeUi(), FakeAiReader())

    expected_line = f'text: "word", coordinates: {Point(1, 2)} {Point(3, 4)} '
    assert printed == [expected_line]


def test_get_text_perform_and_reload_behaviour():
    screenshot = FakeImage(numpy.array([[1, 2], [3, 4]]))
    ai = FakeAiReader([TextData('word', [Point(1, 1), Point(2, 2)])])
    ui = FakeUi(screenshot)
    instruction = GetText(Point(5, 6), Point(10, 12), reload_every_try=False)

    instruction.perform(ui, ai)
    instruction.perform(ui, ai)

    assert screenshot.crop_calls == [(5, 6, 10, 12)]
    assert len(ai.calls) == 1
    assert instruction.local_answer == [TextData('word', [Point(1, 1), Point(2, 2)])]
    assert instruction.global_answer == [TextData('word', [Point(6, 7), Point(7, 8)])]
    assert instruction.screenshot is screenshot
