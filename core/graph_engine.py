# app/core/graph_engine.py

import time
from typing import Any, Dict, List

from app.core.models import (
    GraphMeta,
    RunState,
    RunStatus,
    ExecLogEntry,
)
from app.core.registry import tool_registry
from app.storage.memory import save_run, get_graph

# Import workflow functions (extract_functions, etc.)
from app.workflows import code_review


class GraphEngine:
    """
    Main graph execution engine.
    Handles:
    - Node calling
    - State passing
    - Branching
    - Looping
    - Logging
    """

    def __init__(self):
        pass

    # ---------------------- Node Execution --------------------------

    def _execute_node(self, node_def, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes one node.
        Node can be:
        - A Python function (workflow node)
        - A tool (registered in tool_registry)
        """
        func_name = node_def.func

        if func_name is None:
            raise ValueError(f"Node '{node_def.name}' has no function assigned")

        # 1. Try tool registry
        try:
            func = tool_registry.get(func_name)
        except KeyError:
            # 2. Try workflow functions
            if hasattr(code_review, func_name):
                func = getattr(code_review, func_name)
            else:
                raise ValueError(
                    f"Function '{func_name}' not found as tool or workflow function"
                )

        # Execute node function
        result = func(
            state=state,
            config=node_def.config or {}
        )

        if not isinstance(result, dict):
            raise ValueError(f"Node '{node_def.name}' must return a dict")

        # Update shared state
        state.update(result)
        return state

    # ---------------------- Logging --------------------------

    def _log(self, run: RunState, node_name: str, action: str, msg: str = None):
        entry = ExecLogEntry(
            timestamp=time.time(),
            node=node_name,
            action=action,
            message=msg,
            state_snapshot=run.state.copy(),
        )
        run.logs.append(entry)

    # ---------------------- Branching Logic --------------------------

    def _choose_next_nodes(self, graph: GraphMeta, node_name: str, state: Dict[str, Any]) -> List[str]:
        """
        Basic branching: return next nodes if any.
        """
        return graph.edges.get(node_name, [])

    # ---------------------- Workflow Execution (with loop stop) --------------------------

    def run_graph(self, run: RunState) -> RunState:
        """
        Execute graph until:
        - no next nodes OR
        - quality_score >= threshold (loop stop)
        """

        graph = get_graph(run.graph_id)
        if not graph:
            raise ValueError("Graph not found")

        run.status = RunStatus.RUNNING
        save_run(run)

        current = run.current_node or graph.start_node

        # NEW: threshold for stopping loop (default = 8)
        threshold = run.state.get("threshold", 8)

        try:
            while current:

                run.current_node = current
                node_def = next(n for n in graph.nodes if n.name == current)

                # Log start
                self._log(run, current, "start", f"Running {current}")

                # Run node
                updated_state = self._execute_node(node_def, run.state)

                # Log end
                self._log(run, current, "end", f"Completed {current}")

                save_run(run)

                # ⭐ NEW: Stop loop if quality_score >= threshold
                if updated_state.get("quality_score", 0) >= threshold:
                    self._log(
                        run,
                        current,
                        "stop",
                        f"Stopping loop: quality_score {updated_state.get('quality_score')} >= threshold {threshold}"
                    )
                    break

                # Normal branching
                next_nodes = self._choose_next_nodes(graph, current, updated_state)

                if not next_nodes:
                    break

                # Only one next node for minimal design
                current = next_nodes[0]

            run.status = RunStatus.FINISHED

        except Exception as e:
            run.status = RunStatus.FAILED
            run.error = str(e)
            self._log(run, current, "error", str(e))

        save_run(run)
        return run


# Global engine instance
engine = GraphEngine()
