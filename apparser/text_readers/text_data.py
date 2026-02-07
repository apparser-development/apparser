from dataclasses import dataclass

from apparser.core.geometry import Point


@dataclass(frozen=True)
class TextData:
    text: str
    coordinates: list[Point]
