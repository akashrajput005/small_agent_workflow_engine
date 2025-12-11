from typing import Dict, Callable, Optional


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, func: Callable) -> None:
        self._tools[name] = func

    def get(self, name: str) -> Optional[Callable]:
        return self._tools.get(name)


registry = ToolRegistry()