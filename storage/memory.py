# app/storage/memory.py

"""
A very lightweight in-memory storage layer.

Stores:
- Graphs
- Runs (execution state)
This is enough for the assignment. Can be swapped later for DB.
"""

from typing import Dict
from uuid import UUID
from threading import Lock

from app.core.models import GraphMeta, RunState


# ----------------- Thread Safety -----------------

_graph_lock = Lock()
_run_lock = Lock()


# ----------------- In-Memory Stores -----------------

GRAPHS: Dict[UUID, GraphMeta] = {}
RUNS: Dict[UUID, RunState] = {}


# ----------------- Graph Operations -----------------

def save_graph(graph: GraphMeta):
    """Store a graph by id."""
    with _graph_lock:
        GRAPHS[graph.id] = graph


def get_graph(graph_id: UUID) -> GraphMeta:
    """Retrieve a stored graph."""
    return GRAPHS.get(graph_id)


# ----------------- Run Operations -----------------

def save_run(run: RunState):
    """Add or update a run."""
    with _run_lock:
        RUNS[run.run_id] = run


def get_run(run_id: UUID) -> RunState:
    """Retrieve a run."""
    return RUNS.get(run_id)
