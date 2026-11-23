# DocuMind: Technical Decisions

Last updated: 2026-11-23 (P1.6 results recorded)

Status legend: **Accepted** = approved by the owner. **Provisional** = sensible default, to be tuned or verified. **Deferred** = decided later, after live checks.

## Revision log

- 2026-11-20: Phase 0 approved. Seven refinements added: TD-004 (embedding swap and re-index), TD-006 (security), TD-007 (durable processing), TD-008 (evaluation), TD-009 (single-user, multi-user ready), TD-010 (Git and GitHub), TD-011 (free-plan workflow).
- 2026-11-20: TD-007 **replaces** the earlier plan to use FastAPI BackgroundTasks. BackgroundTasks do not survive a restart, so we use a database-backed job queue with one in-process worker.
- 2026-11-21: Collaboration and deployment plans recorded as TD-013 (two-person Git workflow) and TD-014 (deployment constraints and guardrails). The approved architecture is unchanged. TD-010 gains one rule: once a collaborator joins, nothing goes straight to `main`.
- 2026-11-21: P1.4 findings recorded as TD-015 (Windows development conventions: run Python tools as `python -m`, `httpx2` as the test client). TD-013 gains the merge-method rule.
- 2026-11-22: P1.5 findings recorded as TD-016 (ChromaDB kept, PyMuPDF 1.28.2 pinned, dependency check script) and TD-017 (PyMuPDF licence, decision open). TD-012 updated. TD-001, TD-014 and TD-015 gain one note each.
- 2026-11-23: P1.6 findings recorded as TD-018 (frontend toolchain: exact versions, Tailwind 4 as a Vite plugin, Oxlint instead of ESLint, ports). TD-001 gains one note.

---

## TD-001 Technology stack (Accepted)

- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Lucide Icons, React Router, TanStack Query, react-pdf (PDF preview and jump to page; confirm in Phase 6). Vite, React, TypeScript, Tailwind and Lucide are installed and locked in `frontend/package-lock.json` (P1.6, TD-018). React Router, TanStack Query and react-pdf are added when a screen needs them.
- **Backend:** Python 3.12, FastAPI, Uvicorn, Pydantic, SQLAlchemy 2.x, pytest. Alembic migrations are added in Phase 9, when the schema has settled.
- **Document processing:** PyMuPDF 1.28.2 (text per page, page metadata, PDF outline). Its licence is AGPL-3.0 or commercial, see TD-017.
- **Storage:** SQLite in WAL mode now, PostgreSQL later through SQLAlchemy. ChromaDB 1.5.9 (embedded) for vectors, confirmed in P1.5 (TD-016).
- **AI:** hosted LLM and hosted embeddings behind provider interfaces (TD-004). Providers are Deferred (TD-012).
- **Tooling:** VS Code, Git, GitHub. FastAPI's built-in `/docs` page replaces Postman.
- **Deliberately not used:** Docker (heavy on 8 GB RAM), local models, Celery or Redis, LangChain or LlamaIndex (the RAG pipeline is a few hundred lines; writing it ourselves means it is understood and has fewer dependencies).
- Exact versions are pinned in Phase 1 from installs the owner has verified.

## TD-002 Structure and layering (Accepted)

- Monorepo: `frontend/`, `backend/`, `docs/`.
- Backend layering: **routes → services → repositories and providers**. Routes never call an AI provider or the database directly.
- Prompts live in `backend/app/prompts/` as separate, versioned files.
- No provider SDK is imported outside `backend/app/providers/`.

## TD-003 Persistence and data model (Accepted, draft schema)

- SQLite is the source of truth for documents, chunk text and metadata, chats, summaries and jobs.
- ChromaDB holds vectors plus minimal metadata and can always be rebuilt from SQLite.
- PDFs live on disk at `backend/storage/users/<user_id>/documents/<uuid>.pdf`.

Draft tables (key columns only):

- `users`: id, email (nullable), password_hash (nullable), created_at.
- `documents`: id, user_id, display_name, stored_filename (uuid), size_bytes, sha256, page_count, status, status_detail, index_profile_id, chunker_version, created_at. Unique on (user_id, sha256).
- `chunks`: id, document_id, user_id, chunk_index, page_start, page_end, section, text, embedding_profile_id (nullable until embedded).
- `embedding_profiles`: id, provider, model, dimensions, input_scheme, is_active, created_at.
- `processing_jobs`: see TD-007.
- `conversations`, `conversation_documents`, `messages`, `message_citations` (message_id, chunk_id, label).
- `summaries`, `study_sets`: document_id, kind, content_json, prompt_version, created_at (Phases 7 and 8).

## TD-004 Swappable embeddings, model tracking and re-indexing (Accepted)

Requirement: change the embedding provider without rewriting the RAG pipeline; store model information; support re-indexing.

1. The pipeline depends only on two interfaces. `EmbeddingProvider` has `embed_documents`, `embed_query`, `provider_id`, `model_name` and `dimensions`. `VectorStore` has `upsert`, `query`, `delete_by_document` and `count`.
2. An `embedding_profiles` row identifies a provider, model, dimension count and input scheme. Exactly one profile is active, taken from `.env`.
3. Every embedded chunk records its `embedding_profile_id`. Each profile has its own Chroma collection (`chunks_<profile_id>`), so vectors from different models can never be mixed. A dimension mismatch on write is a hard error.
4. At startup the app compares `.env` with the active profile. If they differ, it registers the new profile and marks existing documents `needs_reindex`. It never mixes models silently.
5. Search covers only documents indexed with the active profile. Others show "Needs re-index".
6. A **re-index job** re-embeds the stored chunk text into the new collection. It does not re-read the PDF or re-chunk. Old vectors are deleted only after the new index for that document is complete, so a failure leaves the old index intact. Re-index is resumable (TD-007).
7. Re-index can run per document or for all documents. It shows a chunk and token estimate first, because free-tier quotas are limited.
8. Changing the chunking method is a separate "reprocess" action, tracked by `chunker_version`.
9. Evaluation reports record the embedding profile (TD-008).

## TD-005 RAG pipeline and citation integrity (Accepted)

- **Ingestion:** validate, store under a UUID name, extract per page, flag pages without text, chunk within page boundaries (about 1,000 characters, small overlap, section taken from the PDF outline when present), embed in batches, mark ready.
- **Answering:** rewrite the follow-up into a standalone question, search only the selected documents, apply a relevance gate (if nothing relevant, answer "not found" without calling the LLM), send labeled sources [S1]…[Sn] to the LLM, and require it to answer only from them.
- **Citation integrity:** the model returns the labels it used. The backend validates them against the retrieved chunks and fills in the real document, page and verbatim snippet from the database. The model never writes page numbers. Messages store chunk IDs, not copied text.
- Uploaded text is untrusted data (prompt-injection stance). The UI distinguishes quoted document text from AI-written explanation.
- Chunk size, overlap and top-k are Provisional and tuned with the evaluation framework (TD-008).

## TD-006 Document security (Accepted)

**Upload validation** (server-side, before any processing):
- Extension `.pdf` AND magic bytes `%PDF-` AND PyMuPDF can open it and finds at least one page. The client-declared MIME type is ignored.
- The upload is streamed to a temporary file with a running size check, never loaded whole into memory.
- Provisional defaults, all in `.env`: 25 MB per file, 500 pages per file, 50 documents and 500 MB per user.
- Encrypted or password-protected PDFs are rejected with a clear message (v1).
- Stored as `<uuid>.pdf`. The original name is sanitized and kept only as display metadata. It is never used to build a path.
- SHA-256 per user: uploading an identical file returns the existing document instead of creating a duplicate.
- PDFs are treated as untrusted input: text extraction only, nothing is executed. Isolating the parser in a separate process is reviewed in Phase 10.

**Access control:**
- Every request resolves a `current_user` dependency (TD-009). Repositories require a `user_id`, and unscoped query functions do not exist.
- Another user's document returns 404, not 403, so existence is not leaked.
- Vector queries always carry user and document filters, but only after ownership of the requested documents is verified in SQLite. The vector filter is a second layer.
- PDFs are served only through an authenticated endpoint (no static folder), with `X-Content-Type-Options: nosniff`.
- From Phase 3, isolation tests create a second user directly in the database and assert that no endpoint leaks across users, even before login exists.

**Safe deletion** (a durable job, so it can resume after a crash):
1. Mark the document `deleting`. It disappears from lists and search at once.
2. Delete its vectors from every collection, then verify the count is zero.
3. Delete the PDF file.
4. Delete chunks, summaries, study sets and citations (database cascade).
5. Delete the document row last.
If any step fails, the document stays `deleting` and is retried, including by a startup sweep. Conversations about only that document are deleted with it. Citations elsewhere show "source removed".

**Secrets and logging:** API keys live only in the backend `.env`. Document text and document-bearing prompts are never logged, and error messages never echo file contents.

## TD-007 Durable document processing (Accepted, replaces BackgroundTasks)

Requirement: survive restarts, track status, support retry, prevent duplicate processing.

- **Queue:** a `processing_jobs` table plus one in-process worker started in the FastAPI lifespan. Concurrency is 1, which suits the i3 and API quotas.
- **Job fields:** id, document_id, job_type (`ingest`, `reindex`, `delete`), status (`queued`, `running`, `succeeded`, `failed`), stage (`extract`, `chunk`, `embed`, `finalize`), attempts, max_attempts (default 3), error_code, error_message, heartbeat_at, timestamps.
- **Duplicate prevention:** a partial unique index on (document_id, job_type) where status is `queued` or `running`. The worker claims a job with an atomic `UPDATE ... WHERE status='queued'` and proceeds only if exactly one row changed. Identical re-uploads are handled by TD-006.
- **Restart recovery:** at startup, `running` jobs return to `queued` (attempts are kept, and jobs over the maximum become `failed`). A stale heartbeat (older than about 2 minutes) also counts as orphaned, which covers the `--reload` double-process case. Documents in `deleting` are resumed.
- **Idempotent stages:** chunks are replaced in one transaction. The embed stage embeds only chunks that have no vector for the active profile. Chroma writes use `upsert` with deterministic IDs (`chunk_<id>`), so repeating a stage is safe.
- **Retry:** transient errors (rate limit, network) retry automatically with exponential backoff up to the maximum. Permanent errors (corrupt file, encrypted file, no extractable text) fail with a readable message and no automatic retry. `POST /documents/{id}/retry` resumes a failed document from the failed stage.
- **Status for the UI:** document status is `pending`, `processing`, `ready`, `failed`, `needs_reindex` or `deleting`, plus stage, progress (chunks embedded of total) and error. The frontend polls with TanStack Query.
- SQLite runs in WAL mode with a busy timeout.

## TD-008 RAG evaluation framework (Accepted, built from Phase 5)

Location: `backend/evals/` with `datasets/` (JSONL cases), `fixtures/` (small self-authored or public-domain PDFs only), `run_eval.py`, `metrics.py` and `reports/`.

**Case types:** answerable, unanswerable, follow-up (with history), injection (the document contains instructions), and multi-document later. Start with about 30 to 40 hand-written cases.

**Metrics, cheapest first:**
- **Retrieval quality:** hit@k, recall@k and MRR against expected pages. This needs embeddings only, no LLM calls.
- **Answer accuracy:** required key facts present, by normalized string or regex match. An LLM judge is optional and off by default to save quota.
- **Citation correctness:** validity (every cited label maps to a retrieved chunk, which must be 100%), page precision and recall against expected pages, and snippet support.
- **Hallucination handling:** correct "not found" rate on unanswerable questions, false-refusal rate on answerable ones, and a check for numbers or names in the answer that appear in no retrieved chunk.

**Rules:**
- Evals call the same service functions as the app, never a separate code path.
- Flags `--retrieval-only`, `--limit N` and `--dry-run` (estimates API calls) protect quotas.
- Each report records the git commit, embedding profile, chunker version, prompt version and LLM model, and is compared against a committed baseline to catch regressions.
- Pass targets are set after the first baseline run, not guessed now.
- Placement: retrieval eval in Phase 5, answer, citation and hallucination eval in Phase 6, expansion in Phase 10.

## TD-009 Single-user development, multi-user ready (Accepted)

- `AUTH_MODE=single_user` is the only mode until Phase 9. The `users` table exists from the first migration with one seeded local user, and `get_current_user` returns it.
- Every user-owned table has a non-null `user_id`. File paths include the user ID, and vector metadata carries it.
- Phase 9 swaps the implementation of one dependency and adds password hashing, tokens, login and register screens, Alembic and rate limiting. It requires no data-model or service rewrite, and the Phase 3 isolation tests prove it.
- Lightweight development: no Docker, no Redis, one worker, SQLite WAL, Vite dev server.

## TD-010 Git and GitHub workflow (Accepted)

- The repository is initialized in Phase 1 before any application code. The first commit is `.gitignore` plus a stub README.
- The GitHub remote starts **private**. It becomes public in Phase 11 after a secret scan.
- Gitignored: `.env`, `storage/`, virtual environments, `node_modules`, uploaded PDFs, Chroma data and eval reports (except the committed baseline). `.env.example` is committed.
- `main` always works. Each milestone gets its own branch (for example `p1-backend-scaffold`), merged through a pull request. Docs-only fixes may go straight to `main` while the owner works alone. Once a collaborator joins, every change goes through a pull request (TD-013).
- Commits follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `refactor:`), small and specific.
- **Milestone Definition of Done:**
  1. It works, verified by the owner running it.
  2. Tests pass.
  3. `PROJECT_STATE.md` and `TASKS.md` are updated, plus any other doc it affects.
  4. It is committed with a meaningful message and pushed.
  5. A phase-end tag `phase-N-complete` is created when a phase finishes.

## TD-011 Working within free-plan usage limits (Accepted)

- A milestone is one verifiable outcome, about 5 files at most, ending in a working state and a commit. Every milestone is a safe pause point.
- Planning is just-in-time. The roadmap details the current phase's milestones and outlines later phases.
- Complete code only for files created or changed. The owner pastes back errors or the last ~20 lines of output, and uses `git diff` for reviews.
- `PROJECT_STATE.md` is updated at every milestone, so a usage limit never strands the project. A Handoff Report is produced on request and saved in `docs/handoffs/`.
- **Verification honesty:** Claude's chat sandbox cannot install packages, so "verified" means the owner ran it and pasted the result. Anything else is labeled "written, not yet run".
- Documents are created only when a milestone needs them.

## TD-012 Deferred decisions

| Decision | When | How |
|---|---|---|
| Embedding provider (for example Voyage AI or Gemini) | Phase 5 | Check live free-tier limits, then choose |
| LLM provider | Phase 6 | Check live free-tier limits, then choose |
| react-pdf vs simpler PDF viewer | Phase 6 | Try react-pdf first |
| ChromaDB vs SQLite plus NumPy fallback | Phase 1 (P1.5) | **Resolved 2026-11-22: ChromaDB 1.5.9 kept** (TD-016). The fallback stays possible behind `VectorStore` |
| PyMuPDF licence: keep it with an AGPL-3.0 repository, or switch to a permissive PDF library | Before the collaborator is invited (P1.7) | See TD-017 |
| Chunk size, overlap, top-k | Phases 5 and 6 | Tune against evals |
| Upload limit values | Phase 4 | Adjust after testing real PDFs |
| Cross-origin auth method (tokens vs cookies) | Phase 9 | Decide with separate frontend and backend domains in mind (TD-014) |
| Backend host (needs always-on process and a persistent disk) | Phase 11 | Re-check live pricing and limits, then choose (TD-014) |
| Vercel plan vs making the repository public | Phase 11 | See TD-014 |

## TD-013 Two-person Git workflow (Accepted, details Provisional)

Context: the owner owns the GitHub repository `documind`. A friend joins as a collaborator and both contribute to the same repository.

- **Ownership and timing:** the owner owns the repository. The friend is invited at the end of Phase 1, once `SETUP_GUIDE.md` exists, so they can set up the same environment from it. Each person sets their own GitHub noreply commit email.
- **No direct pushes to `main`** once the collaborator joins. Every change is a branch, then a pull request, then review and merge by the *other* person.
- **Enforcement:** GitHub's documentation says rulesets are available on GitHub Free only for public repositories, and for private repositories they need Pro or Team. We could not confirm from the documentation whether the older branch protection settings are available for private repositories on Free. Until we check the repository's Settings page, the rule is by agreement. Rulesets become available on Free when the repository goes public (Phase 11).
- **Branch names:** `<yourname>/<milestone-id>-<topic>`, for example `sujal/p2-1-design-tokens`. One milestone has one author.
- **Avoid collisions:** both agree in `TASKS.md` who is on which milestone before starting. Prefer splitting by area (`frontend/` and `backend/`).
- **Shared files** (`PROJECT_STATE.md`, `TASKS.md`, `TECHNICAL_DECISIONS.md`): updated only inside the pull request that completes a milestone, after pulling the latest `main`. Changes to `TECHNICAL_DECISIONS.md` need both people to agree in the pull request.
- **Claude sessions:** each person uses their own Claude account and usage limits. `PROJECT_STATE.md` in the repository is the shared handoff, pasted into a fresh chat.
- **Commits:** Conventional Commits, meaningful messages, authored under each person's own GitHub account so the contribution history is accurate for both.
- **Merging:** pull requests are merged with GitHub's "Create a merge commit" option, so every meaningful commit stays in the history. The branch is deleted after merging, and everyone updates local `main` before starting the next milestone.

## TD-014 Deployment plan, constraints and guardrails (Plan Accepted, hosts Deferred, nothing deployed before Phase 11)

Plan: GitHub holds the source. Vercel hosts the React + Vite frontend (the `frontend/` folder set as the project root). A separate host runs the FastAPI backend, the background worker and the persistent data. One live URL is shared in both LinkedIn posts.

**Constraints found on 2026-11-21 (from the providers' own documentation and comparison articles; re-check before deploying):**
- **Vercel Hobby and collaborators:** Vercel's documentation says the Hobby plan does not support collaboration for private repositories, and that a commit is deployed only if its author is the owner of the Hobby team. Collaboration is free for public repositories, and Pro is the paid alternative. Plan: make the repository public in Phase 11 (already planned, after a secret scan), or use Pro. Vercel is not involved before then.
- **Vercel cannot host the backend.** The backend needs an always-on process (the in-process worker, TD-007), a persistent disk (SQLite, uploaded PDFs, ChromaDB), and exactly one running instance (single SQLite writer, single worker).
- **Free backend hosting is weak for that shape.** Per a Render article and a comparison page: Render's free web services sleep after 15 minutes idle and no free persistent disk is listed; its free Postgres expires after 30 days. Railway's free plan has a small monthly credit and a 0.5 GB volume, and a paid plan of about $5 per month is recommended for persistent uptime. Fly.io has no free tier for new users. Oracle Cloud's Always Free VM exists but needs a credit card and self-management. The Phase 11 decision is between a small paid plan and a free tier with visible trade-offs. TD-007 restart recovery means a sleeping or restarted worker does not lose jobs.
- **Architecture unchanged.** TD-001 already names PostgreSQL as the later path. If no suitable host offers a persistent volume, switching storage would be a new decision recorded here.
- **ChromaDB's size (found in P1.5, TD-016).** It brings dozens of dependencies. That is fine on the owner's laptop, but at P11.2 check that the chosen host has enough memory and disk for the backend with ChromaDB loaded. The `VectorStore` interface (TD-004) allows a lighter store if needed.
- **PyMuPDF licence (TD-017).** A public network deployment is the case the AGPL covers, so that decision is made before Phase 11 and before the collaborator is invited.

**Guardrails before any public URL exists:**
1. Phase 9 authentication is complete. `AUTH_MODE=single_user` must never be exposed publicly, because anyone could read the seeded user's documents and spend the owner's API quota.
2. Per-user daily limits on uploads, questions and re-indexing, tighter upload sizes for the demo, a quota cap, and friendly handling of provider rate-limit errors.
3. A visible notice that uploaded text is sent to third-party AI providers, with working document deletion (TD-006).
4. Secrets only as host environment variables. The frontend receives only `VITE_API_BASE_URL`, which is public by design. Never put keys in `VITE_` variables. Backend CORS allows only the Vercel domain(s). HTTPS only.
5. The frontend never hardcodes `localhost`: the API address comes from `VITE_API_BASE_URL` starting in P1.7.
6. Frontend and backend run on different domains, so the token-versus-cookie decision (SameSite, CORS credentials) is made in Phase 9 with that in mind.
7. Deployment files and a `DEPLOYMENT.md` are written in Phase 11, with separate development and production configuration.

## TD-015 Windows development conventions (Accepted)

Found while building P1.4 on Windows 11 Home with Smart App Control active (2026-11-21).

- **Run Python tools as modules:** `python -m pip`, `python -m pytest`, `python -m uvicorn`. Windows 11's Smart App Control blocked `pip.exe`, one of the small unsigned launcher programs that virtual environments generate, with the message "An Application Control policy has blocked this file". `pytest.exe` and `uvicorn.exe` are the same kind of launcher, so we avoid all of them. `python.exe` is signed and allowed, so the module form works. The compiled packages (pydantic-core, watchfiles, httptools) loaded without problems on the owner's machine. Do not turn off Windows security to work around this.
- **Test client:** `httpx2` (2.16.2) is pinned in `requirements-dev.txt`, not `httpx`. Starlette's `TestClient` now tries `httpx2` first and warns that using `httpx` is deprecated. `httpx2` is a fork of httpx 0.28.1 with the same public API and needs Python 3.11 or newer. Since P1.5, ChromaDB's dependencies install `httpx` 0.28.1 again next to `httpx2`. Starlette still prefers `httpx2`, and pytest showed no warning in a freshly rebuilt environment (2026-11-22).
- **Virtual environment:** `backend/.venv`, created with `py -3.12` (Python 3.12.10) because the machine's default `python` is 3.15. Activation with `.\.venv\Scripts\Activate.ps1` worked without changing PowerShell's script policy.
- **Pinning:** `requirements.txt` pins only the packages we use directly. Their dependencies float within compatible ranges.

## TD-016 Vector store and PDF library confirmed (Accepted)

Found while running the P1.5 dependency spike on the owner's laptop (Windows 11 Home, Python 3.12.10), 2026-11-21 and 2026-11-22. It settles the ChromaDB row of TD-012.

- **ChromaDB 1.5.9 is kept.** It installed from a prebuilt Windows wheel with no compiler and nothing blocked, then passed a functional check run by `backend/scripts/check_dependencies.py`: three vectors written by one Python process, the folder reopened by a second process (restart persistence), a nearest-neighbour search that returned the right id, metadata and text, and deletion by a `document_id` filter, which is the operation safe deletion needs (TD-006). The SQLite plus NumPy fallback is not needed now. The `VectorStore` interface (TD-004) stays, so we can still switch.
- **Telemetry is off.** The check opens ChromaDB with `anonymized_telemetry=False`. The application must do the same when it opens the store in Phase 5.
- **Size.** ChromaDB pulls in dozens of dependencies (among them grpcio, kubernetes, opentelemetry, onnxruntime and tokenizers). We use none of the AI parts, because embeddings come from a provider (TD-004). The size is fine on the laptop and is a check at P11.2 (TD-014).
- **PyMuPDF is pinned to 1.28.2.** PyMuPDF 2.1 was tried first and pulled in heavy extra dependencies. A `pip install --dry-run` showed 1.28.2 needs none. It passed the check: a 2-page PDF with an outline was created, saved, reopened, and its text and outline read back.
- **Repeatable proof.** `python scripts/check_dependencies.py` prints one `PASS` or `FAIL` line per library. A new library gets one function and one line in `CHECKS`.
- **Reproducibility proven.** The virtual environment was deleted and rebuilt from `requirements-dev.txt` alone, and the checks and pytest all passed. The requirements files are complete for this machine.

## TD-017 PyMuPDF licence (Provisional, decision due before the collaborator is invited)

Facts, from Artifex's licensing documentation read on 2026-11-21 (not legal advice; re-read the current terms before deciding): PyMuPDF is dual-licensed under the GNU AGPL-3.0 or a commercial licence from Artifex. Artifex states that offering software built on it as a network service requires making the full source of that software available under the AGPL, unless a commercial licence is bought. DocuMind is planned as a public network service (TD-014), so the question applies from Phase 11.

Options:
- **A. Keep PyMuPDF and release DocuMind under AGPL-3.0.** The repository becomes public in Phase 11 anyway, so publishing the source costs a portfolio project nothing. Consequence: the AGPL then applies to our code and to anyone who reuses it.
- **B. Switch to a library with a permissive licence** (for example pypdf or pdfminer.six). That allows a permissive licence such as MIT for our code. Consequence: re-test text quality, page metadata, outline support, speed and scanned-page detection, and redo the P1.5 check.

Current lean: A. Not final.

Guardrails that hold either way:
- PDF extraction is built behind an interface in Phase 4 (P4.3), with no PyMuPDF import outside it, so switching later is one adapter.
- Decide before the collaborator is invited (P1.7), because the licence changes what contributors are agreeing to, and before the repository is made public (P11.1). Add a matching `LICENSE` file when decided.

## TD-018 Frontend toolchain confirmed (Accepted)

Found while building P1.6 on the owner's laptop (Windows 11 Home, Node 24.22.3, npm 11.19.1), 2026-11-22 and 2026-11-23.

- **Generated with** `npm create vite@latest frontend -- --template react-ts --no-interactive` (create-vite 9.3.4), after checking Vite's official guide (Node 20.19+ or 22.12+ required).
- **Exact versions** are locked in `frontend/package-lock.json`. `package.json` uses ranges such as `^`, so the lock file is what makes installs identical, and it is committed: Vite 8.3.8, React and React DOM 19.3.1, TypeScript 7.0.2, Tailwind CSS 4.3.5 with `@tailwindcss/vite` 4.3.5, lucide-react 1.78.0, `@vitejs/plugin-react` 6.3.0 and Oxlint 1.94.0. Installing and building reported 0 vulnerabilities.
- **Tailwind 4 is a Vite plugin.** `vite.config.ts` lists `tailwindcss()` next to `react()`, and `src/index.css` is the single line `@import "tailwindcss";`. There is no `tailwind.config` file and no PostCSS setup. Colours, fonts, spacing and dark mode become design tokens in CSS in Phase 2 (P2.1). The colours on the placeholder page are not part of the design.
- **Oxlint instead of ESLint.** The current Vite template ships Oxlint (`npm run lint`, configured in `.oxlintrc.json`). We keep it: it is the template default, it adds no extra dependency, and it reported 0 warnings and 0 errors. The ESLint editor extension is not used for the frontend.
- **Icons:** `lucide-react` with named imports only (`import { FileText } from 'lucide-react'`), so unused icons are not bundled. Decorative icons get `aria-hidden="true"`.
- **Scripts and ports:** `npm run dev` (port 5173), `npm run build` (`tsc -b && vite build`, output in `dist/`, ignored by Git), `npm run lint`, and `npm run preview` (serves `dist/` on port 4173). The backend uses port 8000. The browser treats these as different origins, so the backend must allow the frontend's origin (CORS), which P1.7 sets up from configuration.
- **Windows:** Vite 8, Tailwind 4.3 and Oxlint all ran with Smart App Control active and nothing was blocked. TD-015's rule about running tools as modules is specific to Python.
- **Not added yet:** React Router, TanStack Query and react-pdf wait until a screen needs them (Phases 2 and 6).
- **Starter files removed:** the demo page, `App.css`, the logos, `icons.svg` and the starter README. A DocuMind favicon (`public/favicon.svg`) and the page title `DocuMind` replace them. The template's own `frontend/.gitignore` is kept next to the root one.
- **Clean install:** a rebuild of `node_modules` from the lock file with `npm ci` is part of the P1.7 rehearsal, the same way the Python environment was rebuilt in P1.5.
