# app/workflows/code_review.py

"""
Code Review Mini-Agent Workflow
--------------------------------

Nodes implemented:
1. extract_functions
2. check_complexity
3. detect_issues
4. suggest_improvements

This workflow runs until `quality_score >= threshold`.
"""

from typing import Dict, Any


# ---------------- Node Functions -----------------

def extract_functions(state: Dict[str, Any], config: Dict[str, Any]):
    """
    Extracts simple function blocks based on keyword 'def'.
    Purely rule-based, no parsing.
    """
    code = state.get("code", "")
    functions = [line.strip() for line in code.split("\n") if line.strip().startswith("def ")]

    return {
        "functions": functions,
        "num_functions": len(functions),
    }


def check_complexity(state: Dict[str, Any], config: Dict[str, Any]):
    """
    Computes very basic complexity score based on loops & conditions.
    """
    code = state.get("code", "")
    complexity = code.count("for") + code.count("while") + code.count("if")

    return {"complexity": complexity}


def detect_issues(state: Dict[str, Any], config: Dict[str, Any]):
    """
    Detects simple issue patterns like TODO or fix.
    """
    code = state.get("code", "")
    issues = code.count("TODO") + code.count("fix")

    return {"issues": issues}


def suggest_improvements(state: Dict[str, Any], config: Dict[str, Any]):
    """
    Generates a simple quality score and suggests improvements.
    """
    issues = state.get("issues", 0)
    complexity = state.get("complexity", 0)

    # Simple scoring formula
    score = max(0, 10 - issues - complexity)

    suggestions = []
    if issues > 0:
        suggestions.append("Fix reported issues.")
    if complexity > 3:
        suggestions.append("Reduce complexity by refactoring.")
    if not suggestions:
        suggestions.append("Code looks clean!")

    state["quality_score"] = score

    return {
        "quality_score": score,
        "suggestions": suggestions,
    }


# ---------------- Workflow Node Registration -----------------

"""
We don't auto-register these functions in the global tool registry.
Instead, the engine will call them directly by name if connected later.

To make them available:
In your graph definition, set `func` equal to the function name, e.g.:

{
    "name": "extract",
    "func": "extract_functions"
}

The engine will pick them up because FastAPI's main file imports this module.
"""
