# Simple Workflow / Graph Engine (Code Review Example)

Minimal backend assignment implemented with FastAPI.

## Features

- Nodes as Python functions operating on shared `state` (dict)
- Edges describe node order and simple branching
- Looping for code review quality until threshold or max iterations
- In-memory storage of graphs and runs
- Example workflow: Code Review Mini-Agent (Option A)

## Project Structure

- `app/main.py` – FastAPI app and API endpoints
- `app/engine/` – core workflow engine
- `app/tools/registry.py` – simple tool registry
- `app/workflows/code_review.py` – example workflow and tools

## Running

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload