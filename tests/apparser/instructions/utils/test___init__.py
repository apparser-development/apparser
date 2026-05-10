from __future__ import annotations

from apparser.instructions import utils


def test_instruction_utils_exports_expected_symbols() -> None:
    assert set(utils.__all__) == {"get_instruction_by_id", "get_instruction_by_name"}
