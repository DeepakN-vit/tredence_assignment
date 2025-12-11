Minimal Workflow Engine (FastAPI)

This project implements a small workflow/agent engine inspired by the idea of node-based execution graphs. It is built as part of an AI Engineering internship assignment to demonstrate backend engineering fundamentals, API design, state management, and clean Python structure.

The engine allows you to define nodes, connect them with edges, maintain a shared state, and execute the workflow step-by-step. It includes basic branching, looping with conditions, logging, and tool/function execution.

Project Structure
app/
│
├── main.py                 # FastAPI entrypoint and routes
│
├── core/
│   ├── graph_engine.py     # Workflow engine: execution, loops, branching, logs
│   ├── models.py           # Pydantic models for graph & runs
│   └── registry.py         # Tool registry
│
├── workflows/
│   └── code_review.py      # Sample workflow (Code Review Agent)
│
└── storage/
    └── memory.py           # In-memory storage for graphs and runs


This layout keeps each concern separated and ensures the engine logic is easy to understand and modify.

How to Run the Project
1. Install dependencies
pip install fastapi uvicorn

2. Start the FastAPI server

Run from the project root:

uvicorn app.main:app --reload


The server will start at:

http://127.0.0.1:8000

3. Use the interactive API documentation

Open:

http://127.0.0.1:8000/docs


You can create graphs, run workflows, and inspect results directly from the Swagger UI.

What This Workflow Engine Supports
✔ Node-Based Execution

Each node is a Python function that reads and updates a shared state dictionary.

✔ Shared State

State flows from one node to the next and gets updated along the way.

✔ Directed Edges

Edges determine the path of execution. Example:

"edges": { "extract": ["complexity"] }

✔ Branching

Next node is chosen based on graph edges. Can be extended to condition-based routing.

✔ Looping (with stopping condition)

The engine supports looping through nodes until a condition in the shared state is met.
In the Code Review agent, looping stops when:

quality_score >= threshold

✔ Tool Registry

You can register utility functions that nodes can call during execution.

✔ Execution Logs

Every node execution logs:

start time

end time

state snapshot

messages

✔ FastAPI Endpoints

POST /graph/create → register a new workflow

POST /graph/run → execute a workflow

GET /graph/state/{run_id} → view final state + logs

✔ In-Memory Storage

Graphs and runs are stored in lightweight dictionaries (simple and effective for this assignment).

Example Workflow Included (Code Review Agent)

The sample agent performs:

Extract functions

Measure code complexity

Detect basic issues

Suggest improvements

Loop until the quality score reaches the threshold

All steps are rule-based and require no ML.

How to Create and Run a Workflow
1. Create a Graph (example)
{
  "nodes": [
    {"name": "extract", "func": "extract_functions"},
    {"name": "complexity", "func": "check_complexity"},
    {"name": "issues", "func": "detect_issues"},
    {"name": "improve", "func": "suggest_improvements"}
  ],
  "edges": {
    "extract": ["complexity"],
    "complexity": ["issues"],
    "issues": ["improve"],
    "improve": ["extract"]
  },
  "start_node": "extract"
}

2. Run the Graph
{
  "graph_id": "YOUR_GRAPH_ID",
  "initial_state": {
    "code": "def foo(): pass\n# TODO fix\nfor i in range(3): print(i)",
    "threshold": 7
  }
}

3. View Results

Use:

GET /graph/state/{run_id}


You will receive the final state and a complete execution log.

What I Would Improve With More Time

Async Execution:
Run workflows in the background and return run_id immediately.

WebSocket Log Streaming:
Send live execution updates to the client.

Conditional Branching:
Allow nodes to choose next steps based on state values.

Graph Visualization:
Render the node graph visually for easier debugging.

Persistent Storage:
Store graphs and run histories in a database instead of in memory.

Additional Built-In Workflows:
Add summarization pipelines or data-quality agents.

Final Notes

This project focuses on clean structure and correctness.
The goal is not feature overload but demonstrating:

clear API design

clean Python architecture

state-driven execution

ability to reason in terms of nodes, transitions, and loops

This implementation fulfills all core requirements of the assignment.