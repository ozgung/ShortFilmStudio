ShortFilmStudio
================

A small Google ADK demo that chains multiple LLM agents (Producer → Director/Script writers) to create preproduction assets for a 2-minute short film.

Setup
-----
- Python 3.13 (venv recommended).
- Install deps: `pip install -r requirements.txt`.
- Copy env: `cp .env.sample .env` and set `GOOGLE_API_KEY` (and `GOOGLE_GENAI_USE_VERTEXAI=0` unless you use Vertex AI).

Running
-------
- CLI run: `python app.py` to execute the root agent with the default film subject.
- ADK web UI: `adk web` (from the project root) and select the `agents` app; ensure your `.env` is loaded.

Notes
-----
- Agents live in `agents/` (`agent_producer`, `agent_director`, `agent_writer`) and are wired via `agents/agents_config.py` / `agents/root_agent.yaml`.
- `.gitignore` keeps `.env`, `.venv`, caches, and IDE files out of version control.

Submission Requirements
-----------------------
- Include this README describing the problem, solution, architecture, setup instructions, and diagrams/images where useful.

Diagrams
--------
![System Graph 1](images/graph1.png)
![System Graph 2](images/graph2.png)
![Shooting Script Flow](images/shooting-script.png)
![Agent State](images/state.png)
![Trace View](images/trace.png)
