from __future__ import annotations

from typing import Any

import pytest
from appwindows.geometry import Point

from apparser.geometry.distance import distance


def test_distance_returns_manhattan_distance() -> None:
    assert distance(Point(1, 2), Point(4, 6)) == 7


@pytest.mark.parametrize(
    ("first_point", "second_point"),
    [
        (object(), Point(1, 1)),
        (Point(1, 1), object()),
    ],
)
def test_distance_rejects_invalid_points(first_point: Any, second_point: Any) -> None:
    with pytest.raises(TypeError):
        distance(first_point, second_point)
