from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import uuid

from .engine.workflow import Workflow
from .engine.state import WorkflowRunState
from .workflows.code_review import build_code_review_workflow

app = FastAPI()

# In-memory stores
workflows: Dict[str, Workflow] = {}
runs: Dict[str, WorkflowRunState] = {}


class WorkflowDefinition(BaseModel):
    nodes: Dict[str, str]          # node_name -> tool_name
    edges: List[Dict[str, str]]    # {"source": "...", "target": "..."}
    entry_point: str


class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]


@app.on_event("startup")
async def preload_example_workflow():
    # Preload a fixed example workflow
    wf_id = "code_review_example"
    wf_def = build_code_review_workflow()
    workflows[wf_id] = Workflow(graph_id=wf_id, definition=wf_def)


@app.post("/graph/create")
async def create_graph(defn: WorkflowDefinition):
    graph_id = f"graph_{len(workflows) + 1}"
    workflows[graph_id] = Workflow(graph_id=graph_id, definition=defn.dict())
    return {"graph_id": graph_id}


@app.post("/graph/run")
async def run_graph(req: RunRequest):
    if req.graph_id not in workflows:
        raise HTTPException(status_code=404, detail="graph_id not found")

    graph = workflows[req.graph_id]
    run_id = str(uuid.uuid4())

    run_state = WorkflowRunState(
        run_id=run_id,
        graph_id=req.graph_id,
        state=req.initial_state,
        current_node=graph.entry_point,
        status="running",
        log=[],
    )
    runs[run_id] = run_state

    # Synchronous execution for simplicity
    await graph.run(run_state)

    return {
        "run_id": run_id,
        "final_state": run_state.state,
        "log": run_state.log,
        "status": run_state.status,
    }


@app.get("/graph/state/{run_id}")
async def get_graph_state(run_id: str):
    run = runs.get(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run_id not found")
    return run


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)