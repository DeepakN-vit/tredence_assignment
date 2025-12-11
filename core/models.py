# app/core/models.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID, uuid4

# ---------- Basic types ----------

State = Dict[str, Any]

class NodeType(str, Enum):
    """Useful if later we add different node behaviors (call_tool, builtin, etc.)."""
    PY_FUNC = "py_func"
    TOOL = "tool"

# ---------- Node & Graph models ----------

class NodeDef(BaseModel):
    """
    Definition of a node in the graph.
    - name: unique string id for node
    - type: optional (defaults to python function node)
    - func: name of function or tool to call (the engine will map this)
    - config: optional config dict passed to node at runtime
    """
    name: str = Field(..., description="Unique node id")
    type: NodeType = NodeType.PY_FUNC
    func: Optional[str] = Field(None, description="Function name or tool key the engine will call")
    config: Optional[Dict[str, Any]] = None

class GraphCreateRequest(BaseModel):
    """
    Request body to create a graph.
    - nodes: list of node definitions
    - edges: mapping from node -> list of next nodes
      e.g. {"start": ["analyze"], "analyze": ["finish"]}
    - start_node: which node to start from
    """
    nodes: List[NodeDef]
    edges: Dict[str, List[str]] = Field(default_factory=dict)
    start_node: str

class GraphMeta(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    nodes: List[NodeDef]
    edges: Dict[str, List[str]]
    start_node: str

# ---------- Execution / Run models ----------

class ExecLogEntry(BaseModel):
    timestamp: float
    node: str
    action: str
    message: Optional[str] = None
    state_snapshot: Optional[State] = None

class RunCreateRequest(BaseModel):
    graph_id: UUID
    initial_state: Optional[State] = Field(default_factory=dict)
    run_id: Optional[UUID] = None  # allow client to pass a run_id; otherwise engine generates one

class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    FINISHED = "finished"
    FAILED = "failed"

class RunState(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    graph_id: UUID
    status: RunStatus = RunStatus.PENDING
    state: State = Field(default_factory=dict)
    logs: List[ExecLogEntry] = Field(default_factory=list)
    current_node: Optional[str] = None
    error: Optional[str] = None

class RunResult(BaseModel):
    run_id: UUID
    final_state: State
    logs: List[ExecLogEntry]

# ---------- Simple responses ----------

class CreateGraphResponse(BaseModel):
    graph_id: UUID

class CreateRunResponse(BaseModel):
    run_id: UUID

class MessageResponse(BaseModel):
    message: str
