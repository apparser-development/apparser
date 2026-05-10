from __future__ import annotations

import pytest

from apparser.cv.handlers.base import CvHandlers


def test_cv_handlers_is_abstract() -> None:
    with pytest.raises(TypeError):
        CvHandlers()
