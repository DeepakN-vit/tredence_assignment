# app/core/registry.py

"""
Simple tool registry.

Nodes in the graph can reference tools by name.
The engine can then look up and call them.
"""

from typing import Callable, Dict, Any


class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Callable[..., Any]] = {}

    def register(self, name: str, func: Callable[..., Any]):
        """Register a tool by name."""
        self.tools[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        """Retrieve a tool. Raises error if not found."""
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self.tools[name]


# Global registry instance
tool_registry = ToolRegistry()


# ----------------- Example Tools (Optional) -----------------
# These are simple rule-based tools that will help with the sample workflow.

def count_issues(code: str) -> dict:
    """Dummy rule-based issue detector."""
    issues = code.count("TODO") + code.count("fix")
    return {"issues": issues}

def measure_complexity(code: str) -> dict:
    """Very basic complexity heuristic."""
    complexity = code.count("for") + code.count("while") + code.count("if")
    return {"complexity": complexity}

# Pre-register these tools
tool_registry.register("count_issues", count_issues)
tool_registry.register("measure_complexity", measure_complexity)
