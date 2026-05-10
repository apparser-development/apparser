from __future__ import annotations

import pytest

from apparser.cv.processes.base import CvProcess


def test_cv_process_is_abstract() -> None:
    with pytest.raises(TypeError):
        CvProcess()
