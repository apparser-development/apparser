from pathlib import Path
import sys
import tomllib
import types

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
sys.path.insert(0, str(ROOT))

project_data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]


def _install_ultralytics_stub():
    try:
        import ultralytics
        return ultralytics
    except ModuleNotFoundError:
        ultralytics = types.ModuleType("ultralytics")

        class YOLO:
            def __init__(self, *args, **kwargs):
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

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
]

templates_path = []
html_static_path = ['_static']
exclude_patterns = ["_build", "_build*", "__pycache__", "Thumbs.db", ".DS_Store"]
suppress_warnings = ["ref.python"]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}

add_module_names = False

html_theme = 'shibuya'
html_logo = '_static/apparser.svg'
html_css_files = ['custom.css']
