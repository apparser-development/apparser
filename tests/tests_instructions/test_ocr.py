import sys
import types
from types import SimpleNamespace

import numpy
import pytest
from appwindows.geometry import Point


def _install_optional_dependency_stubs():
    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.device = lambda value: value

        class _Hub:
            @staticmethod
            def load(**kwargs):
                class _Model:
                    def to(self, device):
                        self.device = device

                    def apply_tts(self, **settings):
                        class _Audio:
                            def detach(self):
                                return self

                            def cpu(self):
                                return self

                            def numpy(self):
                                return numpy.array([], dtype=numpy.float32)

                        return _Audio()

                return _Model(), None

        torch.hub = _Hub()
        sys.modules["torch"] = torch

    if "ChatTTS" not in sys.modules:
        chattts = types.ModuleType("ChatTTS")

        class _Chat:
            class InferCodeParams:
                def __init__(self, spk_emb=None):
                    self.spk_emb = spk_emb

            def load(self, **kwargs):
                pass

            def sample_random_speaker(self):
                return "speaker"

            def infer(self, text, params_infer_code=None, **kwargs):
                return [numpy.array([], dtype=numpy.float32)]

        chattts.Chat = _Chat
        sys.modules["ChatTTS"] = chattts


_install_optional_dependency_stubs()

import apparser.instructions.ocr.click_on_text as click_on_text_module
import apparser.instructions.ocr.move_to_text as move_to_text_module
import apparser.instructions.ocr.plot_text as plot_text_module
import apparser.instructions.ocr.text_getter as text_getter_module
from apparser.exceptions import TextNotFoundException
from apparser.geometry import RelativelyPoint
from apparser.instructions.ocr.click_on_text import ClickOnText
from apparser.instructions.ocr.move_to_text import MoveToText
from apparser.instructions.ocr.plot_text import PlotAllText, _Painter
from apparser.instructions.ocr.print_all_text import PrintAllText
from apparser.instructions.ocr.text_getter import GetText
from apparser.text_readers.models.text_data import TextData
from tests.utils.readers import FakeTextReader
from tests.utils.ui import InteractionUi


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

    @property
    def __array_interface__(self):
        return self.array.__array_interface__

    def __array__(self, dtype=None, copy=None):
        return self.array


def test_click_on_text_perform_order(monkeypatch):
    calls = []

    class FakeMoveToText:
        def __init__(self, *args, **kwargs):
            calls.append(("move_init", args, kwargs))

        def perform(self, ui, ai):
            calls.append(("move_perform", ui, ai))

    class FakeSleep:
        def __init__(self, sleep_time):
            calls.append(("sleep_init", sleep_time))

        def perform(self, ui, ai):
            calls.append(("sleep_perform", ui, ai))

    class FakeMouseClick:
        def __init__(self, click_type):
            calls.append(("click_init", click_type))

        def perform(self, ui, ai):
            calls.append(("click_perform", ui, ai))

    monkeypatch.setattr(click_on_text_module, "MoveToText", FakeMoveToText)
    monkeypatch.setattr(click_on_text_module, "Sleep", FakeSleep)
    monkeypatch.setattr(click_on_text_module, "MouseClick", FakeMouseClick)

    ui = InteractionUi()
    ai = FakeTextReader()
    ClickOnText("text", sleep_time_before_move=0.3).perform(ui, ai)

    assert calls[0][0] == "move_init"
    assert calls[1] == ("sleep_init", 0.3)
    assert calls[2] == ("move_perform", ui, ai)
    assert calls[3] == ("sleep_perform", ui, ai)
    assert calls[4][0] == "click_init"
    assert calls[5] == ("click_perform", ui, ai)


def test_move_to_text_find_text_and_property(monkeypatch):
    monkeypatch.setattr(
        move_to_text_module.fuzz,
        "token_sort_ratio",
        lambda needed, text: {"wrong": 10, "best": 95}[text],
    )
    instruction = MoveToText("needle")
    texts = [
        TextData("wrong", [Point(0, 0)]),
        TextData("best", [Point(1, 1)]),
    ]

    found, rating = instruction.find_text(texts)

    assert instruction.text == "needle"
    assert found == texts[1]
    assert rating == 95


def test_move_to_text_perform_success(monkeypatch):
    move_calls = []
    getter = SimpleNamespace(
        global_answer=[
            TextData(
                "target",
                [Point(0, 0), Point(10, 0), Point(10, 20), Point(0, 20)],
            )
        ],
        perform=lambda ui, ai: None,
    )
    ui = InteractionUi(relative_point=Point(2, 3))

    class FakeMouseMove:
        def __init__(self, point):
            move_calls.append(("init", point))

        def perform(self, ui):
            move_calls.append(("perform", ui))

    monkeypatch.setattr(move_to_text_module.fuzz, "token_sort_ratio", lambda needed, text: 100)
    monkeypatch.setattr(move_to_text_module, "MouseMove", FakeMouseMove)

    instruction = MoveToText(
        "target",
        min_similarity=0.9,
        offset=RelativelyPoint(0.5, 0.5),
        text_getter=getter,
    )
    instruction.perform(ui, FakeTextReader())

    assert len(ui.global_calls) == 1
    assert isinstance(ui.global_calls[0], RelativelyPoint)
    assert ui.global_calls[0].x == 0.5
    assert ui.global_calls[0].y == 0.5
    assert ui.local_calls == [Point(2, 3)]
    assert move_calls == [("init", Point(7, 13)), ("perform", ui)]


def test_move_to_text_perform_raises_when_similarity_is_low(monkeypatch):
    getter = SimpleNamespace(
        global_answer=[
            TextData("target", [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
        ],
        perform=lambda ui, ai: None,
    )
    monkeypatch.setattr(move_to_text_module.fuzz, "token_sort_ratio", lambda needed, text: 0)

    with pytest.raises(TextNotFoundException):
        MoveToText("target", min_similarity=1.0, text_getter=getter).perform(
            InteractionUi(),
            FakeTextReader(),
        )


def test_painter_draws_coordinates_and_lines():
    calls = []
    draw = SimpleNamespace(
        rectangle=lambda shape, outline, width: calls.append(
            ("rectangle", shape, outline, width)
        ),
        text=lambda position, text, fill: calls.append(
            ("text", position, text, fill)
        ),
    )
    painter = _Painter(draw, (1, 2, 3, 4))
    data = [TextData("word", [Point(5, -20), Point(15, -20), Point(15, -5), Point(5, -5)])]

    painter.draw(data)

    assert calls == [
        ("text", (65, -15), "word", (1, 2, 3, 4)),
        ("rectangle", [(5, -20), (15, -5)], (1, 2, 3, 4), 1),
    ]


def test_plot_all_text_perform(monkeypatch):
    draw_calls = []
    image = FakeImage(numpy.array([[1, 2], [3, 4]], dtype=numpy.uint8))
    getter = SimpleNamespace(
        local_answer=[TextData("word", [Point(0, 0), Point(10, 0), Point(10, 10), Point(0, 10)])],
        screenshot=image.array,
        perform=lambda ui, ai: None,
    )

    class FakeDraw:
        def rectangle(self, shape, outline, width):
            draw_calls.append(("rectangle", shape, outline, width))

        def text(self, position, text, fill):
            draw_calls.append(("text", position, text, fill))

    monkeypatch.setattr(plot_text_module.Image, "fromarray", lambda screenshot: image)
    monkeypatch.setattr(plot_text_module.ImageDraw, "Draw", lambda screenshot: FakeDraw())

    PlotAllText(text_getter=getter, color_rgba=(1, 2, 3, 4)).perform(
        InteractionUi(),
        FakeTextReader(),
    )

    assert draw_calls == [
        ("text", (60, 10), "word", (1, 2, 3, 4)),
        ("rectangle", [(0, 0), (10, 10)], (1, 2, 3, 4), 1),
    ]
    assert image.show_calls == 1


def test_print_all_text_perform(monkeypatch):
    printed = []
    getter = SimpleNamespace(
        global_answer=[TextData("word", [Point(1, 2), Point(3, 4)])],
        perform=lambda ui, ai: None,
    )
    monkeypatch.setattr("builtins.print", lambda line: printed.append(line))

    PrintAllText(text_getter=getter).perform(InteractionUi(), FakeTextReader())

    expected_line = f'text: "word", coordinates: {Point(1, 2)} {Point(3, 4)} '
    assert printed == [expected_line]


def test_get_text_perform_and_reload_behaviour():
    array = numpy.array([[1, 2], [3, 4]], dtype=numpy.uint8)
    screenshot = FakeImage(array)
    ai = FakeTextReader([TextData("word", [Point(1, 1), Point(2, 2)])])
    ui = InteractionUi(screenshot.array)
    instruction = GetText(Point(5, 6), Point(10, 12), reload_every_try=False)

    original_fromarray = text_getter_module.Image.fromarray
    text_getter_module.Image.fromarray = lambda image: screenshot
    instruction.perform(ui, ai)
    instruction.perform(ui, ai)
    text_getter_module.Image.fromarray = original_fromarray

    assert screenshot.crop_calls == [(5, 6, 10, 12)]
    assert len(ai.calls) == 1
    assert instruction.local_answer == [TextData("word", [Point(1, 1), Point(2, 2)])]
    assert instruction.global_answer == [TextData("word", [Point(6, 7), Point(7, 8)])]
    assert numpy.array_equal(array, instruction.screenshot)
