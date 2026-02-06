from appwindows.geometry import Point


def distance(first_point: Point, second_point: Point) -> float:
    if not isinstance(first_point, Point):
        raise TypeError('First Point must be of type Point')

    if not isinstance(second_point, Point):
        raise TypeError('Second Point must be of type Point')

    return abs(first_point.x - second_point.x) + abs(first_point.y - second_point.y)
