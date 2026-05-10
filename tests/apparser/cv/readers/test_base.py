from __future__ import annotations

import pytest

from apparser.cv.readers.base import CvReader


def test_cv_reader_is_abstract() -> None:
    with pytest.raises(TypeError):
        CvReader()
