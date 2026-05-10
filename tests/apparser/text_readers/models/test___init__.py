from __future__ import annotations

import importlib


def test_text_reader_models_package_imports() -> None:
    module = importlib.import_module("apparser.text_readers.models")

    assert module.__name__ == "apparser.text_readers.models"
