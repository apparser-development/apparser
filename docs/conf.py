import sys
import tomllib
import types
from pathlib import Path
from typing import Any

DOCS: Path = Path(__file__).resolve().parent
ROOT: Path = DOCS.parent
sys.path.insert(0, str(ROOT))

project_data: dict[str, Any] = tomllib.loads(
    (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
)["project"]


def _install_ultralytics_stub() -> types.ModuleType:
    try:
        import ultralytics
        return ultralytics
    except ModuleNotFoundError:
        ultralytics = types.ModuleType("ultralytics")

        class YOLO:
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                self.args = args
                self.kwargs = kwargs

        ultralytics.YOLO = YOLO
        sys.modules["ultralytics"] = ultralytics
        return ultralytics


_install_ultralytics_stub()

project = project_data["name"]
author = ", ".join(item["name"] for item in project_data.get("authors", []))
release = project_data["version"]
version = release

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
]

templates_path: list[str] = []
html_static_path: list[str] = ["_static"]
exclude_patterns: list[str] = [
    "_build",
    "_build*",
    "__pycache__",
    "Thumbs.db",
    ".DS_Store",
]
suppress_warnings: list[str] = ["ref.python"]
autodoc_mock_imports: list[str] = ["pyautogui"]
nitpick_ignore: list[tuple[str, str]] = [
    ("py:class", "abc.ABC"),
    ("py:class", "appwindows.appwindows.Window"),
    ("py:class", "numpy.ndarray"),
    ("py:class", "pybind11_builtins.pybind11_object"),
    ("py:class", "tuple[int"),
    ("py:class", "Window"),
    ("py:exc", "WindowDoesNotValidException"),
]

autosummary_generate: bool = True
autodoc_default_options: dict[str, bool | str] = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

add_module_names: bool = False

html_theme: str = "shibuya"
html_logo: str = "_static/apparser.svg"
html_css_files: list[str] = ["custom.css"]
