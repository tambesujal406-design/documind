# DocuMind: PROJECT STATE

Last updated: 2026-11-21

**How to use this file:** paste it at the start of any new Claude conversation, together with any files being changed. A new conversation must not be assumed to know anything about the project. Once the repository has a collaborator, this file is shared: update it only in the pull request that completes a milestone (TD-013).

## Current phase
Phase 1: Project initialization and environment setup. Phase 0 is complete and approved.

## Current task
**P1.4 Backend scaffold, not started.** First step: create the `backend/` folder and the Python 3.12 virtual environment (`py -3.12`).
P1.3 is completed by the commit that adds this file, `TASKS.md` and the two decision documents. This file describes the state as of that commit.

## Milestone progress (Phase 1)
| ID | Milestone | Status |
|---|---|---|
| P1.1 | Environment audit | Done |
| P1.2 | Git and GitHub identity | Done |
| P1.3 | Repository skeleton and first commit | Done |
| P1.4 | Backend scaffold | Not started |
| P1.5 | Dependency spike (PyMuPDF, ChromaDB) | Not started |
| P1.6 | Frontend scaffold | Not started |
| P1.7 | Connect, setup guide, invite collaborator, close phase | Not started |

## Completed
- Phase 0: architecture, RAG pipeline design, folder structure, risk list, workflow and roadmap approved. Seven refinements added (`TECHNICAL_DECISIONS.md`, TD-004 to TD-011).
- P1.1: every tool below was checked and confirmed by the owner, one step at a time.
- P1.2: Git identity set, GitHub email privacy switched on, private repository created.
- P1.3: project folder, Git repository, remote `origin`, `.gitignore` and `README.md` (first commit `f85128b`, pushed to GitHub, confirmed by the owner's push output), then the project documents and `TASKS.md` in the commit that finishes the milestone. The `frontend/` and `backend/` folders appear with their first files, because Git does not track empty folders.
- Features: none built yet.

## Files created or modified
In the Git repository (`C:\dev\documind`):
- `.gitignore`: committed in `f85128b` and pushed.
- `README.md`: stub, committed in `f85128b` and pushed.

Added by the commit that finishes P1.3:
- `TECHNICAL_DECISIONS.md`, `DEVELOPMENT_ROADMAP.md`, `PROJECT_STATE.md`, `TASKS.md`.

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
Confirmed installed on the owner's laptop (Windows 10 Home, 64-bit):
| Tool | Version | Notes |
|---|---|---|
| Git | 2.56.0 | `init.defaultBranch` set to `main`; commit email is the GitHub noreply address |
| Python | 3.12.10 | Use `py -3.12` for DocuMind. Also installed: 3.15.2 (default), 3.14, 3.13 (Store) |
| Node.js | 24.22.3 | Vite 8 needs 20.19+ or 22.12+ |
| npm | 11.19.1 | |
| VS Code | 1.147.0 (x64) | Extensions installed: Python, Pylance, ESLint, Tailwind CSS IntelliSense (plus Claude Code, Live Server) |

Project dependencies (FastAPI, React, ChromaDB and so on) are not installed yet. Versions are pinned when they are.

## Commands to run the application
None yet.

## Tests performed and results
None yet (no application code exists). Environment checks are listed above.

## Known bugs and unresolved issues
- No bugs (no application code exists).
- Unverified: PowerShell script-execution policy (affects `npm` and virtual-environment activation). We will find out in P1.4 and P1.6 and fix it then if needed.
- Open risks: ChromaDB installation on Windows (spike in P1.5), free-tier API quotas, scanned PDFs without text.
- Deployment constraints (TD-014): Vercel Hobby does not support collaboration on private repositories; free backend hosting is weak for a persistent-disk, always-on service. Both are Phase 11 decisions.
- Deferred decisions: embedding provider (Phase 5), LLM provider (Phase 6), PDF viewer (Phase 6), backend host and Vercel plan (Phase 11), cross-origin auth method (Phase 9). See TD-012.

## Owner environment
Windows 10 laptop, 8 GB RAM, Intel Core i3, integrated graphics, 512 GB storage. Free Claude plan with usage limits. Project folder: `C:\dev\documind`. Repository: https://github.com/tambesujal406-design/documind.git (private).

## Working agreements
- One setup step at a time, each command explained, wait for the owner's confirmation.
- Do not repeat completed checks. Do not overwrite or recreate existing files or working configuration.
- Small milestones, each with a meaningful commit and updated docs (TD-010, TD-011).
- `PROJECT_STATE.md` is updated after every completed milestone.
- "Verified" means the owner ran it and reported the result.
- Complete code for every created or changed file, with exact file paths.

## Exact next steps
1. P1.4: create the `backend/` folder, the Python 3.12 virtual environment and a FastAPI `/health` endpoint with a passing pytest.
2. P1.5: PyMuPDF and ChromaDB install spike.
3. P1.6 and P1.7: frontend scaffold, connection to the backend, `SETUP_GUIDE.md`, invite the collaborator, tag `phase-1-complete`.
