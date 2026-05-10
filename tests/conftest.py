from __future__ import annotations

import shutil
from pathlib import Path
from collections.abc import Iterator

import pytest

from tests.utils.external_stubs import install_external_stubs, reset_external_stubs


install_external_stubs()
temp_dir = Path(__file__).resolve().parent / "_tmp"


@pytest.fixture(autouse=True)
def reset_external_modules() -> Iterator[None]:
    shutil.rmtree(temp_dir, ignore_errors=True)
    reset_external_stubs()
    yield
    shutil.rmtree(temp_dir, ignore_errors=True)
