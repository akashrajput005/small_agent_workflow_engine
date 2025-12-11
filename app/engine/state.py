from typing import Dict, Any, List
from pydantic import BaseModel


class WorkflowRunState(BaseModel):
    run_id: str
    graph_id: str
    state: Dict[str, Any]
    current_node: str
    status: str           # "running" | "completed" | "failed"
    log: List[str]