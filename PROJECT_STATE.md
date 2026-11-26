# DocuMind: PROJECT STATE

Last updated: 2026-11-26

**How to use this file:** paste it at the start of any new Claude conversation, together with any files being changed. A new conversation must not be assumed to know anything about the project. Once the repository has a collaborator, this file is shared: update it only in the pull request that completes a milestone (TD-013).

## Current phase
Phase 1: Project initialization and environment setup. Phase 0 is complete and approved.

## Current task
**P1.7b Close Phase 1 is finished on branch `sujal/p1-7b-close-phase-1` and is waiting for its pull request to be merged.** This file describes the state as of that merge. Remaining owner steps: commit and push the documentation update, open the pull request (#5), merge it with "Create a merge commit", delete the branch, update local `main`. Then, on `main`: invite the friend as a collaborator with the Write role and check whether rulesets or branch protection are available on the private repository (TD-013), and create the tag `phase-1-complete`. Record the invitation date and the tag in the next documentation update (P2.1).
After that the next task is **Phase 2, P2.1: design tokens, light and dark theme, layout shell**, on a new branch `sujal/p2-1-design-tokens-and-layout`.
P1.7a was merged earlier by pull request #4 (merge commit `14b703b`).

## Milestone progress (Phase 1)
| ID | Milestone | Status |
|---|---|---|
| P1.1 | Environment audit | Done |
| P1.2 | Git and GitHub identity | Done |
| P1.3 | Repository skeleton and first commit | Done |
| P1.4 | Backend scaffold | Done |
| P1.5 | Dependency spike (PyMuPDF, ChromaDB) | Done |
| P1.6 | Frontend scaffold | Done |
| P1.7a | Connect frontend and backend (settings, CORS, status badge) | Done |
| P1.7b | Close Phase 1: clean-install rehearsal, setup guide, lint plan, licence decision, README | Done (pending merge). Invite collaborator and tag follow the merge |

## Completed
- Phase 0: architecture, RAG pipeline design, folder structure, risk list, workflow and roadmap approved. Seven refinements added (`TECHNICAL_DECISIONS.md`, TD-004 to TD-011).
- P1.1: every tool below was checked and confirmed by the owner, one step at a time.
- P1.2: Git identity set, GitHub email privacy switched on, private repository created.
- P1.3: project folder, Git repository, remote `origin`, `.gitignore`, `README.md` (commit `f85128b`) and the project documents with `TASKS.md` (commit `9fc6099`), both pushed to GitHub.
- P1.4: `backend/` folder, Python 3.12 virtual environment, FastAPI app with `GET /health`, first pytest passing, server run and `/health` and `/docs` checked in the browser by the owner. Merged by pull request #1 (feature commit `c41ed55`, merge commit `e6f6787`).
- P1.5: PyMuPDF 1.28.2 and ChromaDB 1.5.9 installed, pinned and proven by `backend/scripts/check_dependencies.py`. ChromaDB is kept (TD-016). The PyMuPDF licence question is recorded as an open decision (TD-017). The virtual environment was deleted and rebuilt from `requirements-dev.txt` alone, and every check passed. Merged by pull request #2 (feature commit `d3da4e9`, docs commit `340a6a9`, merge commit `8320643`).
- P1.6: `frontend/` app generated with create-vite 9.3.4 (React and TypeScript), Tailwind CSS 4.3.5 added as a Vite plugin, lucide-react 1.78.0 added, starter demo files removed, own favicon and page title added. A placeholder page proves all of it. Lint, production build and a preview of the built app all checked by the owner. Merged by pull request #3 (feature commit `7886dda`, docs commit `b5fa6a9`, merge commit `9616ff7`) (TD-018).
- P1.7a: the backend reads its settings from `backend/app/config.py` and allows the frontend's origin through CORS, with 6 new tests (7 passed in total). The frontend reads the API address from `VITE_API_BASE_URL`, calls `GET /health` and shows the result as a status badge on the home page. The owner saw the badge go green with both servers running, red with the backend stopped, and green again after restarting it (TD-019). Merged by pull request #4 (commits `48c5bf3` backend, `c6c0634` frontend, `2b44274` docs; merge commit `14b703b`). Windows blocked `npm run lint` during this milestone (see Known issues).
- P1.7b: the clean-install rehearsal passed on both sides (frontend: `node_modules` deleted, `npm ci`, build output identical to the previous build; backend: `.venv` deleted and rebuilt from `requirements-dev.txt`, 7 tests passed, both dependency checks passed). `SETUP_GUIDE.md` was written from the confirmed steps (commit `7d798ef`). Licence decided: keep PyMuPDF and release DocuMind under AGPL-3.0 (TD-017, now Accepted). The `LICENSE` file holds the AGPL-3.0 text: commit `9305ef8` held the plain GPL-3.0 text by mistake and commit `3d62e66` replaced it, after a check of the title line and section 13 caught the error. `README.md` was rewritten (commit `8e161f6`). `backend/.env` and `frontend/.env.local` are both confirmed ignored by Git. A provisional plan for the blocked lint tool is recorded in TD-018.
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

Added by P1.7b (branch `sujal/p1-7b-close-phase-1`), all in the repository root:
- `SETUP_GUIDE.md` (new, Windows setup), `LICENSE` (new, AGPL-3.0 text), `README.md` (rewritten: status, stack, setup pointer, document index, licence).
- Updated in the P1.7b documentation commit: `PROJECT_STATE.md`, `TASKS.md`, `DEVELOPMENT_ROADMAP.md`, `TECHNICAL_DECISIONS.md` (TD-017 Accepted, TD-018 lint plan).

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
- The owner (GitHub user `tambesujal406-design`) owns the private repository `documind`. A friend will be added as a collaborator at the end of Phase 1, once `SETUP_GUIDE.md` exists and the PyMuPDF licence decision (TD-017) is made. Both are now done. The friend is invited right after pull request #5 is merged, so that `main` already holds the setup guide, the licence and the new README. Not added yet.
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
| pymupdf | 1.28.2 | PDF text, pages and outline (AGPL-3.0 or commercial; DocuMind uses it under AGPL-3.0, TD-017) |
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
- Install exactly what the lock file says (new machine or clean rebuild): `npm ci`. Proven on 2026-11-25: `Remove-Item -Recurse -Force node_modules`, then `npm ci`, then `npm run build` gave an identical build.
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
- 2026-11-24: `git check-ignore -v` confirmed that `backend/.env` is ignored (root `.gitignore` line 3, rule `.env`) and that `frontend/.env.local` is ignored.
- 2026-11-25: frontend clean rebuild: `node_modules` deleted, `npm ci`, then `npm run build` passed with identical output (2133 modules; `index-CnFYzOV-.css` 10.17 kB and `index-BkS5E6j9.js` 225.38 kB). `git status` stayed clean, so `package-lock.json` was not changed. `npm run lint` was blocked a third time, even after the reinstall, and Windows Security showed a notice that it could not confirm who published `oxlint.win32-x64-msvc.node`.
- 2026-11-25: backend clean rebuild: `.venv` deleted and recreated with `py -3.12`, installed from `requirements-dev.txt` alone. `python -m pytest` gave `7 passed`, and `check_dependencies.py` gave `PASS PyMuPDF`, `PASS ChromaDB` and `All checks passed`.
- 2026-11-26: the `LICENSE` file's title line (`GNU AFFERO GENERAL PUBLIC LICENSE`, `Version 3, 19 November 2007`), its line count (661) and its section 13 ("Remote Network Interaction", line 540) were checked.
- Not tested: the dependency checks ran only on the owner's laptop (Windows, Python 3.12.10, Node 24.22.3). The collaborator's machine and the future backend host are untested. A fresh `git clone` followed by `SETUP_GUIDE.md` on a second computer has not been done yet; the collaborator's first setup is that test. The frontend has no automated tests yet. The "Backend address not set" badge was not seen in a browser; only the `api.ts` logic behind it was tested (under Node).

## Known bugs and unresolved issues
- No known bugs.
- **Decided (TD-017, 2026-11-26):** PyMuPDF is AGPL-3.0 or commercial. DocuMind keeps PyMuPDF and is released under AGPL-3.0, with a `LICENSE` file. PDF extraction is still built behind an interface in Phase 4, so switching later stays possible. This is not legal advice.
- Windows 11 Smart App Control blocked `pip.exe` ("An Application Control policy has blocked this file"). Workaround: run Python tools as `python -m ...` (TD-015). Compiled packages loaded fine (pydantic-core, watchfiles, httptools, PyMuPDF, ChromaDB, Vite, Tailwind). Oxlint is the exception since 2026-11-24 (next item). Do not disable Windows security.
- **Oxlint blocked (open, provisional plan, since 2026-11-24).** `npm run lint` failed three times (the third time after a clean `npm ci` on 2026-11-25) with "An Application Control policy has blocked this file", naming `node_modules\@oxlint\binding-win32-x64-msvc\oxlint.win32-x64-msvc.node`. The same lint run passed with 0 warnings on 2026-11-23, and why it changed is unknown. Nothing else is affected: `npm run build` (which includes the TypeScript check), the dev server and Tailwind all work. Smart App Control stays on, because turning it off cannot be undone without resetting Windows. Windows Security said it could not confirm who published that file (it has no publisher signature). Provisional plan (TD-018): keep Oxlint (the template default, no extra packages), treat the TypeScript check in `npm run build` as the frontend's gate on this laptop, and add a GitHub Actions check that runs lint, build and tests on every pull request, where Windows is not involved. That CI milestone is proposed and waits for the owner's confirmation (`TASKS.md`). Switching to ESLint was considered and not chosen, because it adds many packages and its TypeScript 7 support was not checked.
- `gnu.org` could not be reached from the owner's network on 2026-11-26 (PowerShell: unable to connect; browser: connection timed out), while GitHub worked. The AGPL text was taken from GitHub's licence data instead. Any step that needs `gnu.org` may fail on this network.
- The "new pip release available" notice is ignored for now (pip is 25.0.1).
- VS Code showed one "Error refreshing packages" notice from its Python Environments extension on 2026-11-23. It did not affect the project and was not investigated.
- Open risks: free-tier API quotas, scanned PDFs without text, ChromaDB's size and memory on a small backend host (check in P11.2, TD-014). The ChromaDB install risk on Windows is retired.
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
1. Finish P1.7b: commit and push the documentation update on `sujal/p1-7b-close-phase-1`, open pull request #5, merge with "Create a merge commit", delete the branch, update local `main`.
2. On `main` after the merge: invite the friend as a collaborator (Write role) and check whether branch protection or rulesets are available on the private repository (TD-013). Create and push the tag `phase-1-complete`. Record both in the P2.1 documentation update.
3. Decide whether to add the proposed GitHub Actions check (lint, build and tests on every pull request), which also gets around the Oxlint block (TD-018).
4. Phase 2, starting with P2.1 (design tokens, light and dark theme, layout shell), on a new branch `sujal/p2-1-design-tokens-and-layout`.
