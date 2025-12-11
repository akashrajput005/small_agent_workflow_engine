from typing import Dict, Any, Callable, Optional
import inspect


class Node:
    def __init__(self, name: str, tool_name: str, func: Optional[Callable]):
        self.name = name
        self.tool_name = tool_name
        self.func = func

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not self.func:
            return {}

        try:
            if inspect.iscoroutinefunction(self.func):
                result = await self.func(state)
            else:
                result = self.func(state)
            return result or {}
        except Exception as e:
            # Record error in state; keep it simple
            state["error"] = f"Node {self.name} failed: {e}"
            return {}