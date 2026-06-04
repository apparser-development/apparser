from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest
from appwindows.geometry import Point

from apparser.movers.math_antirobot import AntiRobotMover, DefaultMoveGenerator
from tests.utils import pyautogui_stub


@pytest.mark.parametrize(
    ("kwargs", "error_type"),
    [
        ({"min_time": "0.1"}, TypeError),
        ({"max_time": "2"}, TypeError),
        ({"min_shift": "30"}, TypeError),
        ({"max_shift": "100"}, TypeError),
        ({"min_shift": 10, "max_shift": 5}, ValueError),
        ({"min_time": 2, "max_time": 1}, ValueError),
        ({"min_time": -0.1}, ValueError),
    ],
)
def test_default_move_generator_validates_init_arguments(
    kwargs: dict[str, Any],
    error_type: type[Exception],
) -> None:
    with pytest.raises(error_type):
        DefaultMoveGenerator(**kwargs)


def test_default_move_generator_returns_steps(monkeypatch: pytest.MonkeyPatch) -> None:
    generator = DefaultMoveGenerator(min_time=0.1, max_time=1, min_shift=3, max_shift=4)
    values = iter([3.0, 0.5, 3.0, 0.6, 0.7])

    monkeypatch.setattr(
        "apparser.movers.math_antirobot.random.uniform",
        lambda _min, _max: next(values),
    )

    result = list(generator(Point(0, 0), Point(10, 0)))

    assert result == [
        (Point(3, 0), 0.5),
        (Point(6, 0), 0.6),
        (Point(10, 0), 0.7),
    ]


@pytest.mark.parametrize(
    ("start_position", "end_position"),
    [
        (object(), Point(1, 1)),
        (Point(1, 1), object()),
    ],
)
def test_default_move_generator_rejects_invalid_points(start_position: Any, end_position: Any) -> None:
    generator = DefaultMoveGenerator()

    with pytest.raises(TypeError):
        list(generator(start_position, end_position))


def test_antirobot_mover_rejects_invalid_position() -> None:
    mover = AntiRobotMover()

    with pytest.raises(TypeError):
        mover.move(object())


def test_antirobot_mover_uses_generated_path() -> None:
    def fake_generator(start: Point, end: Point) -> Iterator[tuple[Point, float]]:
        assert start == Point(1, 2)
        assert end == Point(10, 20)
        yield Point(3, 4), 0.1
        yield Point(10, 20), 0.2

    pyautogui_stub._position = (1, 2)
    mover = AntiRobotMover(move_generator=fake_generator)

    mover.move(Point(10, 20))

    assert pyautogui_stub.move_calls == [
        {
            "x": 3,
            "y": 4,
            "duration": 0.1,
        },
        {
            "x": 10,
            "y": 20,
            "duration": 0.2,
        },
    ]
