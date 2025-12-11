# app/main.py

from fastapi import FastAPI, HTTPException
from uuid import uuid4, UUID

from app.core.models import (
    GraphCreateRequest,
    GraphMeta,
    CreateGraphResponse,
    RunCreateRequest,
    RunState,
    CreateRunResponse,
    RunResult,
)
from app.core.graph_engine import engine
from app.storage.memory import save_graph, save_run, get_run
from app.workflows import code_review  # ensures workflow functions are imported


app = FastAPI(title="Minimal Workflow Engine", version="1.0")


# --------------------- Graph Creation ---------------------

@app.post("/graph/create", response_model=CreateGraphResponse)
def create_graph(request: GraphCreateRequest):
    """
    Create a graph with nodes and edges.
    """
    graph = GraphMeta(
        nodes=request.nodes,
        edges=request.edges,
        start_node=request.start_node,
    )

    save_graph(graph)
    return CreateGraphResponse(graph_id=graph.id)


# --------------------- Run Graph ---------------------

@app.post("/graph/run", response_model=CreateRunResponse)
def run_graph(request: RunCreateRequest):
    """
    Start a workflow run.
    """
    run_id = request.run_id or uuid4()

    run = RunState(
        run_id=run_id,
        graph_id=request.graph_id,
        state=request.initial_state or {},
        status="pending",
        current_node=None,
    )

    save_run(run)

    # Execute workflow
    engine.run_graph(run)

    return CreateRunResponse(run_id=run_id)


# --------------------- Get Run State ---------------------

@app.get("/graph/state/{run_id}", response_model=RunResult)
def get_graph_state(run_id: UUID):
    """
    Retrieve current state and logs of a workflow run.
    """
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return RunResult(
        run_id=run.run_id,
        final_state=run.state,
        logs=run.logs,
    )


# --------------------- Root ---------------------

@app.get("/")
def root():
    return {
        "message": "Workflow Engine Running",
        "endpoints": {
            "POST /graph/create": "Create a graph",
            "POST /graph/run": "Run a graph",
            "GET /graph/state/{run_id}": "Get run output",
        }
    }
