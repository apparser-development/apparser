from appwindows.geometry import Point


def distance(first_point: Point, second_point: Point) -> float:
    """Calculate the Manhattan distance between two points.

    :param first_point: First point to compare.
    :type first_point: Point
    :param second_point: Second point to compare.
    :type second_point: Point
    :return: Manhattan distance between the points.
    :rtype: float
    :raises TypeError: If either point has an invalid type.
    """
    if not isinstance(first_point, Point):
        raise TypeError('First Point must be of type Point')

    if not isinstance(second_point, Point):
        raise TypeError('Second Point must be of type Point')

    return abs(first_point.x - second_point.x) + abs(first_point.y - second_point.y)
