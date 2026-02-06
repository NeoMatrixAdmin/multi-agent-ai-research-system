from typing import Dict, Any, Callable

class Tool:
    def __init__(self, name: str, func: Callable, reliability: float):
        self.name = name
        self.func = func
        self.reliability = reliability

    def run(self, query: str):
        return self.func(query)


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self.tools[tool.name] = tool

    def get_all(self):
        return list(self.tools.values())
