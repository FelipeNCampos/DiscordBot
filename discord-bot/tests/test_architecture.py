"""Protege as fronteiras para manter regras independentes de frameworks e I/O."""

from __future__ import annotations

import ast
import importlib.util
import sys
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "bot"


@pytest.mark.parametrize("layer", ["domain", "application", "infra", "config", "presentation"])
def test_architecture_has_explicit_layers(layer: str) -> None:
    assert (PACKAGE / layer / "__init__.py").is_file()


@pytest.mark.parametrize("layer", ["domain", "application"])
def test_inner_layers_only_depend_on_standard_library_and_inward_layers(layer: str) -> None:
    allowed_layers = {"domain"} if layer == "domain" else {"domain", "application"}
    violations = []
    for path in (PACKAGE / layer).rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.level:
                    module = "." * node.level + (node.module or "")
                    package = "bot." + ".".join(path.relative_to(PACKAGE).parts[:-1])
                    modules = [importlib.util.resolve_name(module, package)]
                else:
                    modules = [node.module or ""]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:
                continue
            for module in modules:
                parts = module.split(".")
                if parts[0] == "bot":
                    valid = len(parts) > 1 and parts[1] in allowed_layers
                else:
                    valid = parts[0] in sys.stdlib_module_names or parts[0] == "__future__"
                if not valid:
                    violations.append(f"{path.relative_to(PACKAGE)}:{node.lineno}: {module}")
    assert not violations, "Dependências externas no núcleo:\n" + "\n".join(violations)


@pytest.mark.parametrize("layer", ["infra", "presentation"])
def test_adapters_do_not_import_each_other_or_the_composition_root(layer: str) -> None:
    forbidden = "presentation" if layer == "infra" else "infra"
    violations = []
    for path in (PACKAGE / layer).rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            elif isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            else:
                continue
            for module in modules:
                if module.startswith((f"bot.{forbidden}", "bot.config.bootstrap")):
                    violations.append(f"{path.relative_to(PACKAGE)}:{node.lineno}: {module}")
    assert not violations, "Adaptadores acoplados:\n" + "\n".join(violations)
