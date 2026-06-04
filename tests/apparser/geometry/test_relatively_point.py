from __future__ import annotations

from typing import Any

import pytest

from apparser.geometry.relatively_point import RelativelyPoint


def test_relatively_point_stores_coordinates() -> None:
    point = RelativelyPoint(1, -1)

    assert point.x == 1
    assert point.y == -1


@pytest.mark.parametrize("value", ["1", object()])
def test_relatively_point_rejects_invalid_x_type(value: Any) -> None:
    with pytest.raises(TypeError):
        RelativelyPoint(value, 0)


@pytest.mark.parametrize("value", ["1", object()])
def test_relatively_point_rejects_invalid_y_type(value: Any) -> None:
    with pytest.raises(TypeError):
        RelativelyPoint(0, value)


@pytest.mark.parametrize(
    ("x_percent", "y_percent"),
    [
        (-1.1, 0),
        (1.1, 0),
        (0, -1.1),
        (0, 1.1),
    ],
)
def test_relatively_point_rejects_out_of_range_values(x_percent: float, y_percent: float) -> None:
    with pytest.raises(ValueError):
        RelativelyPoint(x_percent, y_percent)
