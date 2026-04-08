import pytest
from appwindows.geometry import Point

from apparser.geometry import RelativelyPoint, distance


def test_distance_validation_and_value():
    with pytest.raises(TypeError, match='First Point must be of type Point'):
        distance('first', Point(0, 0))

    with pytest.raises(TypeError, match='Second Point must be of type Point'):
        distance(Point(0, 0), 'second')

    assert distance(Point(1, 2), Point(4, 8)) == 9


@pytest.mark.parametrize(('x_percent', 'y_percent', 'error', 'message'), [
    ('1', 0, TypeError, 'x_percent must be number'),
    (0, '1', TypeError, 'y_percent must be number'),
    (-2, 0, ValueError, 'x must be between -1 and 1'),
    (0, 2, ValueError, 'y must be between -1 and 1'),
])
def test_relatively_point_validation(x_percent, y_percent, error, message):
    with pytest.raises(error, match=message):
        RelativelyPoint(x_percent, y_percent)


def test_relatively_point_properties():
    point = RelativelyPoint(0.25, -0.5)

    assert point.x == 0.25
    assert point.y == -0.5
