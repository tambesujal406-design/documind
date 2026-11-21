# DocuMind: PROJECT STATE

Last updated: 2026-11-21

**How to use this file:** paste it at the start of any new Claude conversation, together with any files being changed. A new conversation must not be assumed to know anything about the project. Once the repository has a collaborator, this file is shared: update it only in the pull request that completes a milestone (TD-013).

## Current phase
Phase 1: Project initialization and environment setup. Phase 0 is complete and approved.

## Current task
**P1.5 Dependency spike (PyMuPDF, ChromaDB), not started.** First step: create the milestone branch, then install PyMuPDF into the backend virtual environment with `python -m pip install` and check that it imports. Then the same for ChromaDB.
P1.4 is complete when its pull request (branch `sujal/p1-4-backend-scaffold`) is merged into `main`. This file describes the state as of that merge.

## Milestone progress (Phase 1)
| ID | Milestone | Status |
|---|---|---|
| P1.1 | Environment audit | Done |
| P1.2 | Git and GitHub identity | Done |
| P1.3 | Repository skeleton and first commit | Done |
| P1.4 | Backend scaffold | Done |
| P1.5 | Dependency spike (PyMuPDF, ChromaDB) | Not started |
| P1.6 | Frontend scaffold | Not started |
| P1.7 | Connect, setup guide, invite collaborator, close phase | Not started |

## Completed
- Phase 0: architecture, RAG pipeline design, folder structure, risk list, workflow and roadmap approved. Seven refinements added (`TECHNICAL_DECISIONS.md`, TD-004 to TD-011).
- P1.1: every tool below was checked and confirmed by the owner, one step at a time.
- P1.2: Git identity set, GitHub email privacy switched on, private repository created.
- P1.3: project folder, Git repository, remote `origin`, `.gitignore`, `README.md` (commit `f85128b`) and the project documents with `TASKS.md` (commit `9fc6099`), both pushed to GitHub.
- P1.4: `backend/` folder, Python 3.12 virtual environment, FastAPI app with `GET /health`, first pytest passing, server run and `/health` and `/docs` checked in the browser by the owner. Feature commit `c41ed55` on branch `sujal/p1-4-backend-scaffold`.
- Product features: none yet. The backend exposes only `GET /health`.

## Files created or modified
On `main` (pushed): `.gitignore`, `README.md`, `TECHNICAL_DECISIONS.md`, `DEVELOPMENT_ROADMAP.md`, `PROJECT_STATE.md`, `TASKS.md`.

Added by P1.4 (branch `sujal/p1-4-backend-scaffold`):
- `backend/app/__init__.py` (empty), `backend/app/main.py` (FastAPI app and `/health`), `backend/tests/test_health.py`, `backend/requirements.txt`, `backend/requirements-dev.txt` (commit `c41ed55`).
- Updated in the P1.4 documentation commit: `PROJECT_STATE.md`, `TASKS.md`, `DEVELOPMENT_ROADMAP.md`, `TECHNICAL_DECISIONS.md`.

Local only, never committed: `backend/.venv/` (gitignored).

## Architecture (summary, unchanged)
- React + TypeScript + Vite frontend; FastAPI backend (routes, services, repositories and providers).
- SQLite (source of truth) plus ChromaDB (rebuildable vectors); PDFs on disk under per-user folders.
- Swappable `EmbeddingProvider`, `LLMProvider` and `VectorStore` interfaces; embedding profiles tracked for re-indexing.
- Database-backed job queue with one in-process worker for restart-safe processing.
- Single local user until Phase 9, `user_id` everywhere so authentication can be added without a rewrite.
- Evaluation framework in `backend/evals/` from Phase 5.
Details: `TECHNICAL_DECISIONS.md`.

## Collaboration and deployment plan (recorded 2026-11-21, details in TD-013 and TD-014)
- The owner (GitHub user `tambesujal406-design`) owns the private repository `documind`. A friend will be added as a collaborator at the end of Phase 1, once `SETUP_GUIDE.md` exists. Not added yet.
- Both contribute through branches and pull requests, with meaningful commits.
- Deployment target: GitHub for source, Vercel for the React + Vite frontend, a separate host for the FastAPI backend, worker and persistent data. Goal: one live URL shared in both LinkedIn posts.
- **Nothing is deployed before Phase 11.** No public URL before Phase 9 authentication exists.
- The frontend reads the API address from `VITE_API_BASE_URL` (set up in P1.7), never a hardcoded address.

## Technologies and dependencies
Confirmed installed on the owner's laptop (Windows 11 Home Single Language, 64-bit):
| Tool | Version | Notes |
|---|---|---|
| Git | 2.56.0 | `init.defaultBranch` set to `main`; commit email is the GitHub noreply address |
| Python | 3.12.10 | Use `py -3.12` for DocuMind. Also installed: 3.15.2 (default), 3.14, 3.13 (Store) |
| Node.js | 24.22.3 | Vite 8 needs 20.19+ or 22.12+ |
| npm | 11.19.1 | |
| VS Code | 1.147.0 (x64) | Extensions installed: Python, Pylance, ESLint, Tailwind CSS IntelliSense (plus Claude Code, Live Server) |

Backend packages in `backend/.venv`, pinned in `backend/requirements.txt` and `backend/requirements-dev.txt`:
| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.165.0 | Web framework |
| uvicorn[standard] | 0.54.0 | Server |
| pytest | 9.2.0 | Test runner |
| httpx2 | 2.16.2 | Used by Starlette's `TestClient` (replaces httpx, see TD-015) |

Installed automatically and not pinned directly: pydantic 2.14.4, starlette 1.10.0.
Not installed yet: frontend packages, PyMuPDF and ChromaDB (spike in P1.5).

## Commands to run the application
Run these in PowerShell from `C:\dev\documind\backend`.
- Activate the virtual environment (once per terminal window; the prompt then shows `(.venv)`): `.\.venv\Scripts\Activate.ps1`
- Run the API: `python -m uvicorn app.main:app --reload`, then open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs. Stop it with `Ctrl+C`.
- Run the tests: `python -m pytest`
- Rebuild the environment on another machine: `py -3.12 -m venv .venv`, activate it, then `python -m pip install -r requirements-dev.txt`
- Always run Python tools as `python -m ...` (TD-015).

## Tests performed and results
- 2026-11-21: `python -m pytest` gave `1 passed` with no warnings (`tests/test_health.py`).
- 2026-11-21: `python -m pip install -r requirements-dev.txt` found everything already satisfied, so the requirements files match the environment.
- 2026-11-21: the server started with `python -m uvicorn app.main:app --reload`. The owner confirmed `/health` returned `{"status":"ok","service":"documind-api"}` and `/docs` showed the interactive documentation.

## Known bugs and unresolved issues
- No known bugs.
- Windows 11 Smart App Control blocked `pip.exe` ("An Application Control policy has blocked this file"). Workaround: run tools as `python -m ...` (TD-015). The compiled packages (pydantic-core, watchfiles, httptools) loaded fine. Do not disable Windows security.
- The "new pip release available" notice is ignored for now (pip is 25.0.1).
- Open risks: ChromaDB installation on Windows (spike in P1.5), free-tier API quotas, scanned PDFs without text.
- Deployment constraints (TD-014): Vercel Hobby does not support collaboration on private repositories; free backend hosting is weak for a persistent-disk, always-on service. Both are Phase 11 decisions.
- Deferred decisions: embedding provider (Phase 5), LLM provider (Phase 6), PDF viewer (Phase 6), backend host and Vercel plan (Phase 11), cross-origin auth method (Phase 9). See TD-012.

## Owner environment
Windows 11 laptop (an earlier version of this file said Windows 10, which was wrong), 8 GB RAM, Intel Core i3, integrated graphics, 512 GB storage. Free Claude plan with usage limits. Project folder: `C:\dev\documind`. Repository: https://github.com/tambesujal406-design/documind.git (private).

## Working agreements
- One setup step at a time, each command explained, wait for the owner's confirmation.
- Do not repeat completed checks. Do not overwrite or recreate existing files or working configuration.
- Each code milestone is built on its own branch named `sujal/<milestone-id>-<topic>` and merged through a pull request (TD-010, TD-013).
- Small milestones, each with a meaningful commit and updated docs (TD-010, TD-011).
- `PROJECT_STATE.md` is updated after every completed milestone.
- Run Python tools as `python -m ...` (TD-015).
- "Verified" means the owner ran it and reported the result.
- Complete code for every created or changed file, with exact file paths.

## Exact next steps
1. P1.5: create branch `sujal/p1-5-dependency-spike`, install PyMuPDF and ChromaDB with `python -m pip`, check that both import and work, and decide ChromaDB versus the SQLite plus NumPy fallback (TD-012).
2. P1.6 and P1.7: frontend scaffold, connection to the backend, `SETUP_GUIDE.md`, invite the collaborator, tag `phase-1-complete`.
