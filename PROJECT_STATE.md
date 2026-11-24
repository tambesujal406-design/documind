# DocuMind: PROJECT STATE

Last updated: 2026-11-24

**How to use this file:** paste it at the start of any new Claude conversation, together with any files being changed. A new conversation must not be assumed to know anything about the project. Once the repository has a collaborator, this file is shared: update it only in the pull request that completes a milestone (TD-013).

## Current phase
Phase 1: Project initialization and environment setup. Phase 0 is complete and approved.

## Current task
**P1.7a Connect frontend and backend is finished on branch `sujal/p1-7a-connect-frontend-backend` (commit `48c5bf3` for the backend, `c6c0634` for the frontend) and is waiting for its pull request to be merged.** This file describes the state as of that merge. Remaining owner steps: commit and push the documentation update, open the pull request (#4), merge it with "Create a merge commit", delete the branch, update local `main`.
After that the next task is **P1.7b Close Phase 1**, on a new branch `sujal/p1-7b-close-phase-1`: clean-install rehearsal of both sides, `SETUP_GUIDE.md`, a decision about the blocked lint tool, the PyMuPDF licence decision (TD-017) with a matching `LICENSE` file, invite the collaborator, tag `phase-1-complete`.
P1.6 was merged earlier by pull request #3 (merge commit `9616ff7`).

## Milestone progress (Phase 1)
| ID | Milestone | Status |
|---|---|---|
| P1.1 | Environment audit | Done |
| P1.2 | Git and GitHub identity | Done |
| P1.3 | Repository skeleton and first commit | Done |
| P1.4 | Backend scaffold | Done |
| P1.5 | Dependency spike (PyMuPDF, ChromaDB) | Done |
| P1.6 | Frontend scaffold | Done |
| P1.7a | Connect frontend and backend (settings, CORS, status badge) | Done (pending merge) |
| P1.7b | Close Phase 1: clean-install rehearsal, setup guide, lint decision, licence decision, invite collaborator, tag | Not started |

## Completed
- Phase 0: architecture, RAG pipeline design, folder structure, risk list, workflow and roadmap approved. Seven refinements added (`TECHNICAL_DECISIONS.md`, TD-004 to TD-011).
- P1.1: every tool below was checked and confirmed by the owner, one step at a time.
- P1.2: Git identity set, GitHub email privacy switched on, private repository created.
- P1.3: project folder, Git repository, remote `origin`, `.gitignore`, `README.md` (commit `f85128b`) and the project documents with `TASKS.md` (commit `9fc6099`), both pushed to GitHub.
- P1.4: `backend/` folder, Python 3.12 virtual environment, FastAPI app with `GET /health`, first pytest passing, server run and `/health` and `/docs` checked in the browser by the owner. Merged by pull request #1 (feature commit `c41ed55`, merge commit `e6f6787`).
- P1.5: PyMuPDF 1.28.2 and ChromaDB 1.5.9 installed, pinned and proven by `backend/scripts/check_dependencies.py`. ChromaDB is kept (TD-016). The PyMuPDF licence question is recorded as an open decision (TD-017). The virtual environment was deleted and rebuilt from `requirements-dev.txt` alone, and every check passed. Merged by pull request #2 (feature commit `d3da4e9`, docs commit `340a6a9`, merge commit `8320643`).
- P1.6: `frontend/` app generated with create-vite 9.3.4 (React and TypeScript), Tailwind CSS 4.3.5 added as a Vite plugin, lucide-react 1.78.0 added, starter demo files removed, own favicon and page title added. A placeholder page proves all of it. Lint, production build and a preview of the built app all checked by the owner. Merged by pull request #3 (feature commit `7886dda`, docs commit `b5fa6a9`, merge commit `9616ff7`) (TD-018).
- P1.7a: the backend reads its settings from `backend/app/config.py` and allows the frontend's origin through CORS, with 6 new tests (7 passed in total). The frontend reads the API address from `VITE_API_BASE_URL`, calls `GET /health` and shows the result as a status badge on the home page. The owner saw the badge go green with both servers running, red with the backend stopped, and green again after restarting it (TD-019). Commits `48c5bf3` (backend) and `c6c0634` (frontend) on branch `sujal/p1-7a-connect-frontend-backend`. Windows blocked `npm run lint` during this milestone (see Known issues).
- Product features: none yet. The backend exposes only `GET /health`. The frontend shows a placeholder page.

## Files created or modified
On `main` (pushed): `.gitignore`, `README.md`, `TECHNICAL_DECISIONS.md`, `DEVELOPMENT_ROADMAP.md`, `PROJECT_STATE.md`, `TASKS.md`, and the backend: `backend/app/__init__.py` (empty), `backend/app/main.py` (FastAPI app and `/health`), `backend/tests/test_health.py`, `backend/requirements.txt`, `backend/requirements-dev.txt`, `backend/scripts/check_dependencies.py`.

Added by P1.6 (branch `sujal/p1-6-frontend-scaffold`, commit `7886dda`), all in `frontend/`:
- `package.json`, `package-lock.json` (exact versions), `index.html`, `vite.config.ts`, `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`, `.oxlintrc.json`, `.gitignore`.
- `public/favicon.svg` (own icon), `src/main.tsx`, `src/index.css` (the Tailwind import), `src/App.tsx` (placeholder page).
- Updated in the P1.6 documentation commit: `PROJECT_STATE.md`, `TASKS.md`, `DEVELOPMENT_ROADMAP.md`, `TECHNICAL_DECISIONS.md`.

Added by P1.7a (branch `sujal/p1-7a-connect-frontend-backend`):
- Backend (commit `48c5bf3`): `backend/app/config.py` (settings), `backend/.env.example`, `backend/tests/test_cors.py` (6 tests). Changed: `backend/app/main.py` (CORS middleware) and `backend/requirements.txt` (added `pydantic-settings==2.16.3`).
- Frontend (commit `c6c0634`): `frontend/.env.example`, `frontend/src/api.ts` (the only code that calls the backend), `frontend/src/vite-env.d.ts` (types for the environment variable). Changed: `frontend/src/App.tsx`, now showing the backend status badge.
- Updated in the P1.7a documentation commit: `PROJECT_STATE.md`, `TASKS.md`, `DEVELOPMENT_ROADMAP.md`, `TECHNICAL_DECISIONS.md` (new TD-019).

Local only, never committed: `backend/.venv/`, `frontend/node_modules/`, `frontend/dist/`, `frontend/.env.local` (all gitignored; the last one was confirmed with `git check-ignore`).

## Architecture (summary, unchanged)
- React + TypeScript + Vite frontend; FastAPI backend (routes, services, repositories and providers).
- SQLite (source of truth) plus ChromaDB (rebuildable vectors); PDFs on disk under per-user folders.
- Swappable `EmbeddingProvider`, `LLMProvider` and `VectorStore` interfaces; embedding profiles tracked for re-indexing.
- Database-backed job queue with one in-process worker for restart-safe processing.
- Single local user until Phase 9, `user_id` everywhere so authentication can be added without a rewrite.
- Evaluation framework in `backend/evals/` from Phase 5.
Details: `TECHNICAL_DECISIONS.md`.

## Collaboration and deployment plan (recorded 2026-11-21, details in TD-013 and TD-014)
- The owner (GitHub user `tambesujal406-design`) owns the private repository `documind`. A friend will be added as a collaborator at the end of Phase 1, once `SETUP_GUIDE.md` exists and the PyMuPDF licence decision (TD-017) is made. Not added yet.
- Both contribute through branches and pull requests, with meaningful commits.
- Deployment target: GitHub for source, Vercel for the React + Vite frontend, a separate host for the FastAPI backend, worker and persistent data. Goal: one live URL shared in both LinkedIn posts.
- **Nothing is deployed before Phase 11.** No public URL before Phase 9 authentication exists.
- The frontend reads the API address from `VITE_API_BASE_URL` (done in P1.7a, TD-019), never a hardcoded address.

## Technologies and dependencies
Confirmed installed on the owner's laptop (Windows 11 Home Single Language, 64-bit):
| Tool | Version | Notes |
|---|---|---|
| Git | 2.56.0 | `init.defaultBranch` set to `main`; commit email is the GitHub noreply address |
| Python | 3.12.10 | Use `py -3.12` for DocuMind. Also installed: 3.15.2 (default), 3.14, 3.13 (Store) |
| Node.js | 24.22.3 | Vite 8 needs 20.19+ or 22.12+ |
| npm | 11.19.1 | |
| VS Code | 1.147.0 (x64) | Extensions installed: Python, Pylance, ESLint, Tailwind CSS IntelliSense (plus Claude Code, Live Server). The frontend uses Oxlint, so the ESLint extension is unused there (TD-018) |

Backend packages in `backend/.venv`, pinned in `backend/requirements.txt` and `backend/requirements-dev.txt`:
| Package | Version | Purpose |
|---|---|---|
| fastapi | 0.165.0 | Web framework |
| uvicorn[standard] | 0.54.0 | Server |
| pydantic-settings | 2.16.3 | Reads settings from environment variables and a `.env` file (TD-019) |
| pymupdf | 1.28.2 | PDF text, pages and outline (licence: TD-017) |
| chromadb | 1.5.9 | Embedded vector database (TD-016) |
| pytest | 9.2.0 | Test runner (dev) |
| httpx2 | 2.16.2 | Used by Starlette's `TestClient` (dev, see TD-015) |

Installed automatically and not pinned directly: pydantic 2.14.4, starlette 1.10.0, numpy 2.5.5, onnxruntime 1.32.0, and dozens more, mostly ChromaDB's dependencies. `httpx` 0.28.1 is among them (ChromaDB needs it) and sits next to `httpx2` without causing a warning.

Frontend packages in `frontend/node_modules`, exact versions locked in `frontend/package-lock.json` (`package.json` uses ranges):
| Package | Version | Purpose |
|---|---|---|
| vite | 8.3.8 | Dev server and build |
| react, react-dom | 19.3.1 | UI library |
| typescript | 7.0.2 | Type checking (`tsc -b` runs before every build) |
| tailwindcss, @tailwindcss/vite | 4.3.5 | Styling, as a Vite plugin (no config file) |
| lucide-react | 1.78.0 | Icons |
| @vitejs/plugin-react | 6.3.0 | React support in Vite |
| oxlint | 1.94.0 | Code checker (the template's default, TD-018) |
| @types/react, @types/react-dom, @types/node | 19.3.0, 19.3.0, 24.19.2 | Type definitions |

Not installed yet (added when a screen needs them): React Router, TanStack Query, react-pdf.

## Commands to run the application
Backend: run in PowerShell from `C:\dev\documind\backend`.
- Activate the virtual environment (once per terminal window; the prompt then shows `(.venv)`): `.\.venv\Scripts\Activate.ps1`
- Run the API (port 8000): `python -m uvicorn app.main:app --reload`, then open http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs. Stop it with `Ctrl+C`.
- Without activating, from the same folder: `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
- Settings (TD-019): the API works with built-in development defaults. To change one, copy `.env.example` to `.env` and edit it. The server must be started from `backend/`, because it looks for `.env` in the folder it starts in.
- Run the tests: `python -m pytest` (expect `7 passed`)
- Check that PyMuPDF and ChromaDB really work on this machine: `python scripts/check_dependencies.py` (expect two `PASS` lines and `All checks passed`)
- Rebuild the environment (proven on 2026-11-22): `deactivate`, `Remove-Item -Recurse -Force .venv`, `py -3.12 -m venv .venv`, `.\.venv\Scripts\Activate.ps1`, `python -m pip install -r requirements-dev.txt`
- Always run Python tools as `python -m ...` (TD-015).

Frontend: run in PowerShell from `C:\dev\documind\frontend`. The Python environment does not need to be active.
- Install packages (first time, or after `package.json` changes): `npm install`
- First time only (TD-019): `Copy-Item .env.example .env.local`. This holds `VITE_API_BASE_URL=http://127.0.0.1:8000`. Vite reads it when it starts, so restart `npm run dev` after any change. `.env.local` is gitignored.
- Run the app (port 5173): `npm run dev`, then open http://localhost:5173/. Stop it with `Ctrl+C`.
- Run both together: backend in one PowerShell tab (`Ctrl+Shift+T` opens another), frontend in the other. The page badge should read "Backend connected (documind-api)". With the backend stopped it reads "Backend not reachable".
- Check the code: `npm run lint` (blocked by Windows since 2026-11-24, see Known issues). `npm run build` also runs the TypeScript check.
- Build the production version into `dist/`: `npm run build`
- Serve the built version (port 4173): `npm run preview`

## Tests performed and results
- 2026-11-21: `python -m pytest` gave `1 passed` with no warnings (`tests/test_health.py`).
- 2026-11-21: the server started with `python -m uvicorn app.main:app --reload`. The owner confirmed `/health` returned `{"status":"ok","service":"documind-api"}` and `/docs` showed the interactive documentation.
- 2026-11-21: PyMuPDF 1.28.2 passed the check (made a 2-page PDF with an outline, saved it, reopened it, read the text and outline). ChromaDB 1.5.9 installed from a prebuilt Windows wheel and imported.
- 2026-11-22: `python scripts/check_dependencies.py` gave `PASS PyMuPDF` and `PASS ChromaDB` (stored 3 vectors, kept them across a restart in a separate process, found the nearest, deleted one document's vectors), then `All checks passed`. `python -m pytest` gave `1 passed` with no warnings.
- 2026-11-22: the virtual environment was deleted and rebuilt from `requirements-dev.txt` alone. The same checks and pytest passed again, so the requirements files are complete.
- 2026-11-22: `npm install` added 28 packages with 0 vulnerabilities. `npm run dev` started Vite 8.3.8 and the owner confirmed the starter page loaded at http://localhost:5173/ and its counter button worked. After adding Tailwind, the owner confirmed the placeholder page was styled (centered, bold heading, rounded badge).
- 2026-11-23: after adding lucide-react, the owner confirmed the icon tile renders. `npm run lint` gave 0 warnings and 0 errors. `npm run build` passed (2132 modules transformed; JavaScript 223.73 kB, 70.39 kB gzipped; CSS 8.14 kB). `npm run preview` served the built app at http://localhost:4173/ and the owner confirmed the page, the `DocuMind` title and the 412-byte favicon file. The unused starter files were gone.
- 2026-11-23: `python -m pytest` gave `7 passed` on the owner's laptop: the health test plus 6 CORS tests (`tests/test_cors.py`).
- 2026-11-24: frontend `npm run build` passed with the new code (2133 modules transformed; JavaScript 225.38 kB, 71.09 kB gzipped; CSS 10.17 kB). `git check-ignore -v .env.local` showed it is ignored (`frontend/.gitignore` line 13, `*.local`). With both servers running, the owner saw the badge read "Backend connected (documind-api)". With the backend stopped it read "Backend not reachable" with the start hint, and after restarting the backend it was green again. Before that, the logic of `api.ts` was tested under Node with a fake `fetch`: address unset gives `ApiNotConfiguredError` with no network call, a trailing slash is trimmed, and an error status throws.
- 2026-11-24: `npm run lint` failed twice because Windows blocked Oxlint's native file (see Known issues).
- Not tested: the dependency checks ran only on the owner's laptop (Windows, Python 3.12.10, Node 24.22.3). The collaborator's machine and the future backend host are untested. A clean frontend install from the lock file (`npm ci`) has not been run yet; it is planned for P1.7b. The frontend has no automated tests yet. The "Backend address not set" badge was not seen in a browser; only the `api.ts` logic behind it was tested (under Node).

## Known bugs and unresolved issues
- No known bugs.
- **Open decision (TD-017):** PyMuPDF is AGPL-3.0 or commercial. It must be settled before the collaborator is invited: keep PyMuPDF with an AGPL-3.0 repository (current lean), or switch to a permissive PDF library. This is not legal advice.
- Windows 11 Smart App Control blocked `pip.exe` ("An Application Control policy has blocked this file"). Workaround: run Python tools as `python -m ...` (TD-015). Compiled packages loaded fine (pydantic-core, watchfiles, httptools, PyMuPDF, ChromaDB, Vite, Tailwind). Oxlint is the exception since 2026-11-24 (next item). Do not disable Windows security.
- **Oxlint blocked (open, new on 2026-11-24).** `npm run lint` failed twice with "An Application Control policy has blocked this file", naming `node_modules\@oxlint\binding-win32-x64-msvc\oxlint.win32-x64-msvc.node`. The same lint run passed with 0 warnings on 2026-11-23, and why it changed is unknown. Nothing else is affected: `npm run build` (which includes the TypeScript check), the dev server and Tailwind all work. Smart App Control stays on, because turning it off cannot be undone without resetting Windows. Options for P1.7b: look for the block in Windows Security (Protection history), retry after a restart, or move the frontend checker to ESLint (plain JavaScript, but more packages). Until decided, the TypeScript check in `npm run build` is the frontend's gate (TD-018).
- Not yet checked: that a real `backend/.env` file would be ignored by Git. Only `frontend/.env.local` has been checked. Check it in P1.7b before the collaborator is invited, with `git check-ignore -v backend/.env`.
- The "new pip release available" notice is ignored for now (pip is 25.0.1).
- VS Code showed one "Error refreshing packages" notice from its Python Environments extension on 2026-11-23. It did not affect the project and was not investigated.
- Open risks: free-tier API quotas, scanned PDFs without text, ChromaDB's size and memory on a small backend host (check in P11.2, TD-014). The ChromaDB install risk on Windows is retired.
- Deployment constraints (TD-014): Vercel Hobby does not support collaboration on private repositories; free backend hosting is weak for a persistent-disk, always-on service. Both are Phase 11 decisions.
- Deferred decisions: embedding provider (Phase 5), LLM provider (Phase 6), PDF viewer (Phase 6), PyMuPDF licence (before the collaborator joins), backend host and Vercel plan (Phase 11), cross-origin auth method (Phase 9). See TD-012.

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
1. Finish P1.7a: commit and push the documentation update on `sujal/p1-7a-connect-frontend-backend`, open pull request #4, merge it with "Create a merge commit", delete the branch, update local `main`.
2. P1.7b, on branch `sujal/p1-7b-close-phase-1`: check that `backend/.env` is gitignored; rehearse a clean install of both sides (`npm ci`, then the Python rebuild); write `SETUP_GUIDE.md` from the confirmed steps (Windows first); decide what to do about the blocked lint tool (TD-018); make the PyMuPDF licence decision (TD-017) and add the matching `LICENSE` file; update `README.md`; invite the collaborator (Write role) and check whether branch protection or rulesets are available on the private repository (TD-013); tag `phase-1-complete`.
