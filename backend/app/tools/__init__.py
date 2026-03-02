"""Tool registry — auto-discovers tool modules in this package."""

import importlib
import logging
import pkgutil
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

TOOL_PREFIX = "hotel-concierge:"

ToolHandler = Callable[[dict], Coroutine[Any, Any, dict]]

_registry: dict[str, dict] | None = None


def discover_tools() -> dict[str, dict]:
    """Import all sibling modules and collect TOOL_CONFIG + handler."""
    global _registry
    if _registry is not None:
        return _registry

    _registry = {}
    package = importlib.import_module(__package__)
    for info in pkgutil.iter_modules(package.__path__):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{__package__}.{info.name}")
        config = getattr(mod, "TOOL_CONFIG", None)
        handler = getattr(mod, "handler", None)
        if config and handler:
            name = config["name"]
            _registry[name] = {"config": config, "handler": handler}
            logger.info("Registered tool: %s", name)
    return _registry


def get_handler(tool_name: str) -> ToolHandler | None:
    """Look up handler by tool name."""
    registry = discover_tools()
    entry = registry.get(tool_name)
    return entry["handler"] if entry else None
