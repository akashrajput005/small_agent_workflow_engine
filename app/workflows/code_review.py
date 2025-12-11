from typing import Dict, Any
from ..tools.registry import registry


def _extract_functions(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    # toy logic: count "def "
    functions = [f"func_{i}" for i, _ in enumerate(code.split("def ")[1:], start=1)]
    return {"functions": functions}


def _check_complexity(state: Dict[str, Any]) -> Dict[str, Any]:
    func_count = len(state.get("functions", []))
    complexity = func_count * 2
    return {"complexity_score": complexity}


def _detect_issues(state: Dict[str, Any]) -> Dict[str, Any]:
    code = state.get("code", "")
    issues = []

    if "print(" in code:
        issues.append("Debug print statements found")
    if "TODO" in code:
        issues.append("TODO comments present")

    return {"issues": issues, "issue_count": len(issues)}


def _suggest_improvements(state: Dict[str, Any]) -> Dict[str, Any]:
    suggestions = []

    if state.get("complexity_score", 0) > 5:
        suggestions.append("Refactor large functions into smaller ones")

    if state.get("issue_count", 0) > 0:
        suggestions.append("Fix detected issues before merging")

    complexity_penalty = min(state.get("complexity_score", 0), 10)
    issue_penalty = min(state.get("issue_count", 0) * 2, 10)
    quality_score = max(0, 10 - complexity_penalty - issue_penalty)

    return {
        "suggestions": suggestions,
        "quality_score": quality_score,
    }


# Register tools at import time
registry.register("extract_functions", _extract_functions)
registry.register("check_complexity", _check_complexity)
registry.register("detect_issues", _detect_issues)
registry.register("suggest_improvements", _suggest_improvements)


def build_code_review_workflow() -> Dict[str, Any]:
    return {
        "nodes": {
            "extract": "extract_functions",
            "check_complexity": "check_complexity",
            "detect_issues": "detect_issues",
            "suggest_improvements": "suggest_improvements",
        },
        "edges": [
            {"source": "extract", "target": "check_complexity"},
            {"source": "check_complexity", "target": "detect_issues"},
            {"source": "detect_issues", "target": "suggest_improvements"},
        ],
        "entry_point": "extract",
    }