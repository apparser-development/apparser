from dataclasses import dataclass

from appwindows.geometry import Point


@dataclass
class FakeWindowPoints:
    left_top: Point
