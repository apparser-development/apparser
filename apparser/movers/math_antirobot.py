import random
from typing import Generator, Callable

import mouse
from appwindows.geometry import Point

from apparser.geometry import distance
from apparser.movers.base import BaseMover


class DefaultMoveGenerator:
    def __init__(self, min_time: float = 0.1, max_time: float = 2, min_shift: float = 30, max_shift: float = 100):
        if not (isinstance(min_time, float) or isinstance(min_time, int)):
            raise TypeError('min_time must be number')

        if not (isinstance(max_time, float) or isinstance(max_time, int)):
            raise TypeError('max_time must be number')

        if not (isinstance(min_shift, float) or isinstance(min_shift, int)):
            raise TypeError('min_shift must be number')

        if not (isinstance(max_shift, float) or isinstance(max_shift, int)):
            raise TypeError('max_shift must be number')

        if min_shift > max_shift:
            raise ValueError('min_shift must be less than max_shift')

        if min_time > max_time:
            raise ValueError('min_time must be less than max_time')

        if min_time < 0:
            raise ValueError('min_time must be greater than 0')

        self.__min_time = min_time
        self.__max_time = max_time
        self.__min_shift = min_shift
        self.__max_shift = max_shift

    def __get_random_time(self) -> float:
        return random.uniform(self.__min_time, self.__max_time)

    def __get_random_position(self, current_position: Point, end_position: Point) -> Point:
        current_distance = distance(current_position, end_position)
        random_shift = min(random.uniform(self.__min_shift, self.__max_shift), current_distance)

        x_shift = end_position.x - current_position.x
        y_shift = end_position.y - current_position.y

        x_sign = 1 if x_shift >= 0 else -1
        y_sign = 1 if y_shift >= 0 else -1

        x_part = abs(x_shift) / current_distance
        y_part = abs(y_shift) / current_distance

        return Point(round(random_shift * x_part) * x_sign,
                     round(random_shift * y_part) * y_sign)

    def __call__(self, start_position: Point, end_position: Point) -> Generator[tuple[Point, float], None, None]:
        if not isinstance(start_position, Point):
            raise TypeError('start_position must be Point')

        if not isinstance(end_position, Point):
            raise TypeError('end_position must be Point')

        while start_position != end_position:
            if distance(start_position, end_position) <= self.__max_shift:
                yield end_position, self.__get_random_time()
                break
            added_point = self.__get_random_position(start_position, end_position)
            start_position += added_point
            yield start_position, self.__get_random_time()


class AntiRobotMover(BaseMover):
    def __init__(self,
                 move_generator: Callable[[Point, Point], Generator[Point, None, None]] = DefaultMoveGenerator()):
        self.__move_generator = move_generator

    def move(self, position: Point):
        if not isinstance(position, Point):
            raise TypeError('position must be Point')

        current_position = Point(*mouse.get_position())
        for i, t in self.__move_generator(current_position, position):
            mouse.move(i.x, i.y, duration=t)
