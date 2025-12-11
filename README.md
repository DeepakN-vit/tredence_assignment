 
---

# Minimal Workflow Engine (FastAPI)

This project implements a lightweight workflow engine that executes a sequence of connected nodes using shared state. It is designed for evaluating backend fundamentals such as API design, state handling, modular Python architecture, and workflow execution. The system supports node functions, branching, looping with conditions, logging, and extensibility through a tool registry.

---

## Project Structure

```
app/
│
├── main.py
│
├── core/
│   ├── graph_engine.py
│   ├── models.py
│   └── registry.py
│
├── workflows/
│   └── code_review.py
│
└── storage/
    └── memory.py
```

This structure separates routing, engine logic, workflows, storage, and shared utilities for clarity and maintainability.

---

## How to Run the Project

### 1. Install dependencies

```
pip install fastapi uvicorn
```

### 2. Start the FastAPI server

From the project root:

```
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

### 3. Use the interactive documentation

Open:

```
http://127.0.0.1:8000/docs
```

You can create graphs, run workflows, and inspect results through the Swagger interface.

---

## Features Supported by the Workflow Engine

### Node-Based Execution

Nodes are simple Python functions that read from and modify a shared state dictionary.

### Shared State

The state flows through each node and accumulates outputs as execution progresses.

### Directed Edges

Edges describe the execution order among nodes.

Example:

```
"edges": { "extract": ["complexity"] }
```

### Branching

Next nodes are selected based on graph edges. The design supports future extension for conditional branching.

### Looping with Stop Conditions

Node execution can repeat in a loop until a condition in the state is satisfied.
In the Code Review workflow, execution stops when:

```
quality_score >= threshold
```

### Tool Registry

A simple registry enables defining reusable helper functions that can be invoked within nodes.

### Execution Logs

The engine records start and end times of each node along with state snapshots and messages.

### FastAPI Endpoints

* POST `/graph/create`
* POST `/graph/run`
* GET `/graph/state/{run_id}`

### In-Memory Storage

Graphs and runs are stored in lightweight in-memory structures suitable for this assignment.

---

## Example Workflow: Code Review Agent

This sample workflow performs the following:

1. Extract functions
2. Compute basic complexity
3. Detect issues
4. Suggest improvements
5. Loop until the quality score meets the threshold

All operations are simple rule-based checks.

---

## How to Create and Run a Workflow

### 1. Create a graph

```
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
```

### 2. Run the graph

```
{
  "graph_id": "YOUR_GRAPH_ID",
  "initial_state": {
    "code": "def foo(): pass\n# TODO fix\nfor i in range(3): print(i)",
    "threshold": 7
  }
}
```

### 3. View results

```
GET /graph/state/{run_id}
```

The endpoint returns final state updates and a detailed execution log.

---

## Possible Improvements With More Time

* Asynchronous execution to allow background workflow processing
* WebSocket-based streaming of execution logs
* Conditional branching rules inside the graph engine
* Visual representation of the workflow graph
* Database-backed storage for graphs and executions
* Additional predefined workflows such as summarization or data quality checking

---

## Result Screenshots

<p align="center">
  <img width="918" height="497" src="https://github.com/user-attachments/assets/f81f0dc6-5b77-4e82-ac50-66dd1a4e0591" />
</p>

<p align="center">
  <img width="909" height="498" src="https://github.com/user-attachments/assets/3acf1191-3d14-44be-9083-237fefdb19fa" />
</p>

<p align="center">
  <img width="957" height="501" src="https://github.com/user-attachments/assets/fd93e244-48ef-4513-b564-7baffc6a108d" />
</p>

<p align="center">
  <img width="1134" height="495" src="https://github.com/user-attachments/assets/9f2850e6-b5ab-4272-b15a-5a0cefccf0ce" />
</p>

<p align="center">
  <img width="884" height="365" src="https://github.com/user-attachments/assets/43bc360c-eb28-493b-b5fb-5460bdb2650f" />
</p>

<p align="center">
  <img width="1077" height="407" src="https://github.com/user-attachments/assets/e7ca2258-5670-462a-aa9d-246008b9ba76" />
</p>

---

## Final Notes

This project focuses on clarity of design and correctness of execution.
The implementation demonstrates:

* Clean API structure
* Well-separated Python modules
* State-driven workflow execution
* Ability to describe processes using nodes, transitions, and loops

This implementation satisfies all core requirements of the assignment.

---

 
