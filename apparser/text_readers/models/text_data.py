from dataclasses import dataclass

from apparser.geometry import QuadPoints


@dataclass(frozen=True)
class TextData:
    """Store detected text together with its polygon coordinates."""

    text: str
    coordinates: QuadPoints