from dataclasses import dataclass

from base import Point


@dataclass(frozen=True)
class TextData:
    text: str
    coordinates: list[Point]
