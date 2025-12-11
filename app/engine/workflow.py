from typing import Dict, Any, List
from .nodes import Node
from .state import WorkflowRunState
from ..tools.registry import registry


class Workflow:
    def __init__(self, graph_id: str, definition: Dict[str, Any]):
        self.graph_id = graph_id
        self.entry_point: str = definition["entry_point"]

        # node_name -> Node
        self.nodes: Dict[str, Node] = {}
        for node_name, tool_name in definition["nodes"].items():
            tool_func = registry.get(tool_name)
            self.nodes[node_name] = Node(
                name=node_name,
                tool_name=tool_name,
                func=tool_func,
            )

        # adjacency list for edges
        self.edges: Dict[str, List[str]] = {}
        for edge in definition["edges"]:
            src, tgt = edge["source"], edge["target"]
            self.edges.setdefault(src, []).append(tgt)

    async def run(self, run_state: WorkflowRunState) -> None:
        current = run_state.current_node
        visited_count: Dict[str, int] = {}

        while current:
            node = self.nodes[current]
            visited_count[current] = visited_count.get(current, 0) + 1

            run_state.log.append(f"Running node: {current}")
            result = await node.execute(run_state.state)
            run_state.state.update(result)

            # Simple loop + stop condition for code review example:
            # After 'suggest_improvements', if quality_score < threshold,
            # loop back to 'detect_issues' up to 3 iterations.
            if current == "suggest_improvements":
                score = run_state.state.get("quality_score", 0)
                threshold = run_state.state.get("quality_threshold", 7)
                if score < threshold and visited_count[current] < 3:
                    run_state.log.append(
                        f"quality_score={score} < threshold={threshold}, looping"
                    )
                    current = "detect_issues"
                    continue

            # Simple branching support:
            next_nodes = self.edges.get(current, [])
            if not next_nodes:
                break

            if len(next_nodes) == 1:
                current = next_nodes[0]
            else:
                # If multiple, pick based on state["branch"] if present
                branch = run_state.state.get("branch")
                if branch in next_nodes:
                    current = branch
                else:
                    current = next_nodes[0]

        run_state.current_node = current
        run_state.status = "completed"