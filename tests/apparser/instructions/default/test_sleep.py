from __future__ import annotations

import pytest

from apparser.instructions.default.sleep import Sleep


def test_sleep_rejects_non_positive_time() -> None:
    with pytest.raises(ValueError):
        Sleep(0)


def test_sleep_calls_time_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    sleep_calls: list[float] = []
    instruction = Sleep(0.3)
    monkeypatch.setattr("apparser.instructions.default.sleep.time.sleep", lambda value: sleep_calls.append(value))

    instruction.perform()

    assert sleep_calls == [0.3]
    assert instruction.id == 9
