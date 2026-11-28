# DocuMind: Setup Guide (Windows)

Last verified: 2026-11-25, on the project owner's laptop (Windows 11 Home).

This guide takes you from nothing to both DocuMind servers running on your own computer. Every command here has been run on Windows 11. **Other operating systems have not been tested**, so this guide does not cover them yet.

**What you get at this stage:** a backend with one endpoint (`/health`) and a frontend home page that shows whether it can reach the backend. The product features (upload, chat, summaries) are built in later phases (see `DEVELOPMENT_ROADMAP.md`).

## 1. What you need first

| Tool | Version used | Check it with | Notes |
|---|---|---|---|
| Git | 2.56.0 | `git --version` | https://git-scm.com |
| Python | 3.12.10 | `py -3.12 --version` | Install Python 3.12 from https://www.python.org and keep the "py launcher" option ticked. Other versions are not tested. Your default `python` may be a different version, which is why every command below says `py -3.12` |
| Node.js and npm | Node 24.22.3, npm 11.19.1 | `node --version` and `npm --version` | https://nodejs.org. Vite 8 needs Node 20.19 or newer (or 22.12 or newer) |
| VS Code | 1.147.0 | optional | https://code.visualstudio.com |
| GitHub access | | | The repository is public, so anyone can clone it. To push your own branches you must be a collaborator: the owner adds your GitHub account, and you accept the invitation email |

You also need an internet connection for the installs. The first backend install takes a few minutes because ChromaDB brings many packages.

## 2. Get the code

Pick a short folder path, preferably outside OneDrive. The project owner uses `C:\dev`. Run this in PowerShell:

```powershell
cd C:\dev
git clone https://github.com/tambesujal406-design/documind.git
cd documind
```

The first time, Git usually opens a browser window to sign in to GitHub. The rest of this guide assumes the project is in `C:\dev\documind`. Change the paths if yours is elsewhere.

## 3. Backend (Python)

Run these in PowerShell, from the project folder:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest
python scripts/check_dependencies.py
```

What each line does:
- `py -3.12 -m venv .venv` creates a private folder of Python packages for this project, so it cannot clash with anything else on your computer.
- `.\.venv\Scripts\Activate.ps1` switches your PowerShell window to use it. The prompt then starts with `(.venv)`. You need this once per PowerShell window.
- `python -m pip install -r requirements-dev.txt` installs the exact package versions the project uses. A "new release of pip is available" notice is safe to ignore.
- `python -m pytest` runs the tests. Expect `7 passed`.
- `python scripts/check_dependencies.py` proves that PyMuPDF and ChromaDB really work on your machine. Expect `PASS PyMuPDF`, `PASS ChromaDB` and `All checks passed`.

**If PowerShell refuses to run the activate script** (a message about running scripts being disabled), skip activation and start each tool through the environment's own Python instead: `.\.venv\Scripts\python.exe -m pytest`, `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`, and so on.

**Always run Python tools as `python -m ...`** (`python -m pip`, `python -m pytest`, `python -m uvicorn`). On Windows 11 with Smart App Control, the small launcher programs such as `pip.exe` can be blocked ("An Application Control policy has blocked this file"). The `python -m` form is not affected. Do not turn off Windows security to work around it.

### Start the backend

```powershell
python -m uvicorn app.main:app --reload
```

Leave this window open. Open http://127.0.0.1:8000/health in a browser. You should see `{"status":"ok","service":"documind-api"}`. The interactive API documentation is at http://127.0.0.1:8000/docs. Stop the server with `Ctrl+C`.

### Optional backend settings

The backend works with built-in development settings. To change one (for example the browser origins it allows), copy `backend\.env.example` to `backend\.env` and edit it. Start the server from the `backend` folder, because that is where it looks for `.env`. The `.env` file is ignored by Git and never leaves your computer.

## 4. Frontend (React)

Open a **second** PowerShell tab (`Ctrl+Shift+T` in Windows Terminal). The Python environment is not needed here.

```powershell
cd C:\dev\documind\frontend
npm ci
Copy-Item .env.example .env.local
npm run dev
```

What each line does:
- `npm ci` installs the exact package versions recorded in `package-lock.json`. It never changes that file.
- `Copy-Item .env.example .env.local` creates your own settings file. It holds `VITE_API_BASE_URL=http://127.0.0.1:8000`, the address of the backend. The file is ignored by Git. Do this **before** `npm run dev`, because Vite reads it only when it starts. If you change it later, stop and restart `npm run dev`.
- `npm run dev` starts the frontend on http://localhost:5173/.

Every `VITE_` setting is public: it is built into the code the browser downloads. Never put a secret or an API key in one.

## 5. Check that it all works

With the backend and the frontend both running, open http://localhost:5173/. The badge under the DocuMind title shows one of four states:

| Badge | Meaning |
|---|---|
| Checking the backend… (amber, pulsing) | The page is asking. This lasts a moment |
| Backend connected (documind-api) (green) | Everything works |
| Backend not reachable (red) | The backend is not running, or it is not at the address in `.env.local`. Start it as in section 3 |
| Backend address not set (red) | `frontend\.env.local` is missing. Create it as in section 4 and restart `npm run dev` |

To see the red state, stop the backend with `Ctrl+C` and refresh the page. Start the backend again and refresh to get green again.

## 6. Everyday commands

Backend (PowerShell, in `backend`, environment active):

| What | Command |
|---|---|
| Run the API | `python -m uvicorn app.main:app --reload` |
| Run the tests | `python -m pytest` |
| Check PyMuPDF and ChromaDB | `python scripts/check_dependencies.py` |

Frontend (PowerShell, in `frontend`):

| What | Command |
|---|---|
| Run the app | `npm run dev` |
| Build the production version and check the types | `npm run build` |
| Serve the built version on port 4173 | `npm run preview` |
| Check the code style | `npm run lint` (see the known issue below) |

## 7. Known issues

- **`npm run lint` can be blocked on Windows.** Oxlint, the code checker, loads a compiled file that Windows 11 Smart App Control may refuse to run, with the message "An Application Control policy has blocked this file". It was blocked on the project owner's laptop on 2026-11-24 and after a clean reinstall. It is a limit of that Windows setup, not a problem in the code. `npm run build` also runs the TypeScript check, so use it as your check. Do not turn off Smart App Control: Windows cannot turn it back on without being reset. Details are in `TECHNICAL_DECISIONS.md` (TD-018).
- **The browser reports a CORS error.** The backend only accepts pages opened from the addresses in `CORS_ALLOWED_ORIGINS`. The default allows `http://localhost:5173` and `http://127.0.0.1:5173`. If you open the page on another address or port, add it to that setting in `backend\.env` and restart the backend.
- **Two `GET /health` lines in the backend window.** In development, React runs the page's start-up check twice on purpose. This is normal, and the production build asks once.

## 8. Working together

The full rules are in `TECHNICAL_DECISIONS.md` (TD-010, TD-011 and TD-013). In short:
- Never commit straight to `main` (GitHub refuses direct pushes to it). Make a branch named `sujal/<milestone-id>-<topic>` (use your own name in place of `sujal`).
- Commit messages follow Conventional Commits, for example `feat(frontend): show live backend status`.
- Open a pull request and merge it with **Create a merge commit**. Update the documents (`PROJECT_STATE.md`, `TASKS.md`) in the pull request that finishes a milestone.
- Before starting a milestone, put your name in the Owner column of `TASKS.md`.
- The repository is public. Never commit a key, a password or a `.env` file. If you ever push one by mistake, tell the owner straight away so it can be replaced at the provider.

## 9. What has been verified

| Step | Verified |
|---|---|
| Backend: clean rebuild of `.venv` from `requirements-dev.txt`, then tests and the dependency check | Yes, 2026-11-25 |
| Frontend: delete `node_modules`, `npm ci`, then `npm run build` (output identical to the previous build) | Yes, 2026-11-25 |
| Both servers running together, with the badge going green, red and green again | Yes, 2026-11-24 |
| A fresh `git clone` followed by this guide, on a second computer | Not yet. The first collaborator's setup is the real test; fix any gaps in a pull request |
| macOS or Linux | Not tested |
