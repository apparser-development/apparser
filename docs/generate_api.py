from pathlib import Path
import ast
import importlib
import inspect
import sys
import types

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
SOURCE = ROOT / "apparser"
OUTPUT = DOCS / "api"

sys.path.insert(0, str(ROOT))


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

_exports_cache = {}
_module_cache = {}


def _source_path(module_name: str) -> Path:
    parts = module_name.split(".")[1:]
    return SOURCE.joinpath(*parts, "__init__.py")


def _resolve_module(module_name: str, node: ast.ImportFrom) -> str | None:
    if node.level == 0:
        return node.module
    parts = module_name.split(".")
    prefix = parts[:len(parts) - node.level + 1]
    if node.module:
        prefix.extend(node.module.split("."))
    return ".".join(prefix)


def _read_tree(module_name: str) -> ast.Module:
    return ast.parse(_source_path(module_name).read_text(encoding="utf-8"))


def _extract_all(node: ast.AST) -> list[str] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    items = []
    for item in node.elts:
        if isinstance(item, ast.Constant) and isinstance(item.value, str):
            items.append(item.value)
    return items


def _unique(items: list[str]) -> list[str]:
    result = []
    seen = set()
    for item in items:
        if item.startswith("_"):
            continue
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def get_exports(module_name: str) -> list[str]:
    cached = _exports_cache.get(module_name)
    if cached is not None:
        return cached
    explicit = None
    imported = []
    for node in _read_tree(module_name).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    extracted = _extract_all(node.value)
                    if extracted is not None:
                        explicit = extracted
        elif isinstance(node, ast.ImportFrom):
            resolved = _resolve_module(module_name, node)
            for alias in node.names:
                if alias.name == "*":
                    if resolved is not None:
                        imported.extend(get_exports(resolved))
                else:
                    imported.append(alias.asname or alias.name)
    exports = _unique(explicit if explicit is not None else imported)
    _exports_cache[module_name] = exports
    return exports


def get_module(module_name: str):
    module = _module_cache.get(module_name)
    if module is None:
        module = importlib.import_module(module_name)
        _module_cache[module_name] = module
    return module


def get_object(fullname: str):
    module_name, object_name = fullname.rsplit(".", 1)
    return getattr(get_module(module_name), object_name)


def get_kind(obj) -> str:
    if inspect.isclass(obj):
        return "class"
    if inspect.isroutine(obj) or inspect.isbuiltin(obj):
        return "function"
    return "data"


def get_key(obj) -> tuple[str, str, str]:
    return (
        get_kind(obj),
        getattr(obj, "__module__", type(obj).__module__),
        getattr(obj, "__qualname__", getattr(obj, "__name__", type(obj).__qualname__)),
    )


def module_name_for(path: Path) -> str:
    rel = path.relative_to(OUTPUT)
    if not rel.parts:
        return "apparser"
    return "apparser." + ".".join(rel.parts)


def clear_output():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for path in OUTPUT.rglob("*.rst"):
        path.unlink()


def write(path: Path, lines: list[str]):
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_modules_page(paths: list[Path]):
    lines = [
        "API Reference",
        "=============",
        "",
        ".. toctree::",
        "   :maxdepth: 2",
        "",
    ]
    for path in paths:
        lines.append(f"   {path.name}/index")
    write(OUTPUT / "modules.rst", lines)


def build_module_page(path: Path, exports: list[str], children: list[Path]):
    module_name = module_name_for(path)
    lines = [module_name, "=" * len(module_name), ""]
    if children:
        lines.extend(["Children", "--------", "", ".. toctree::", "   :maxdepth: 2", ""])
        for child in children:
            lines.append(f"   {child.name}/index")
        lines.append("")
    if exports:
        lines.extend(["API", "---", "", ".. toctree::", "   :maxdepth: 1", ""])
        for export in exports:
            lines.append(f"   {export}")
        lines.append("")
    write(path / "index.rst", lines)


def build_object_page(path: Path, module_name: str, export: str, kind: str, no_index: bool):
    lines = [export, "=" * len(export), "", f".. currentmodule:: {module_name}", ""]
    if kind == "class":
        lines.append(f".. autoclass:: {export}")
        if no_index:
            lines.append("   :no-index:")
        lines.extend([
            "   :members:",
            "   :undoc-members:",
            "   :show-inheritance:",
            "   :member-order: bysource",
        ])
    elif kind == "function":
        lines.append(f".. autofunction:: {export}")
        if no_index:
            lines.append("   :no-index:")
    else:
        lines.append(f".. autodata:: {export}")
        if no_index:
            lines.append("   :no-index:")
    lines.append("")
    write(path / f"{export}.rst", lines)


def sorted_module_paths() -> list[Path]:
    return sorted(
        (path for path in OUTPUT.rglob("*") if path.is_dir()),
        key=lambda path: (len(path.relative_to(OUTPUT).parts), path.relative_to(OUTPUT).as_posix()),
    )


def main():
    clear_output()

    module_paths = sorted_module_paths()
    top_paths = sorted((path for path in OUTPUT.iterdir() if path.is_dir()), key=lambda path: path.name)
    aliases = []
    exports_by_path = {}
    for path in module_paths:
        module_name = module_name_for(path)
        exports = get_exports(module_name)
        exports_by_path[path] = exports
        for export in exports:
            aliases.append((path, module_name, export))

    canonical = {}
    kinds = {}
    for _, module_name, export in aliases:
        fullname = f"{module_name}.{export}"
        obj = get_object(fullname)
        key = get_key(obj)
        canonical.setdefault(key, fullname)
        kinds[fullname] = get_kind(obj)

    build_modules_page(top_paths)

    for path in module_paths:
        children = sorted((child for child in path.iterdir() if child.is_dir()), key=lambda child: child.name)
        build_module_page(path, exports_by_path[path], children)

    for path, module_name, export in aliases:
        fullname = f"{module_name}.{export}"
        obj = get_object(fullname)
        key = get_key(obj)
        build_object_page(path, module_name, export, kinds[fullname], canonical[key] != fullname)


if __name__ == "__main__":
    main()
