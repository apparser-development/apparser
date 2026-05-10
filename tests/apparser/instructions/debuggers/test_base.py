from __future__ import annotations

import pytest

from apparser.instructions.debuggers.base import BaseDebugger


def test_base_debugger_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseDebugger()
