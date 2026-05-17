from dataclasses import dataclass

from apparser.geometry import Point


@dataclass(frozen=True)
class TextData:
    """Store detected text together with its polygon coordinates."""

    text: str
    coordinates: list[Point]
