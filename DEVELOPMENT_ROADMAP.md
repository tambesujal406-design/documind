# DocuMind: Development Roadmap

Last updated: 2026-11-22

## How to read this

- Phases 0 to 11 keep the original order. No phase is skipped.
- Each phase is split into **milestones** with IDs like `P1.3`. A milestone is one verifiable outcome, about 5 files at most, and ends in a working state and a commit (see TD-010 and TD-011).
- The current phase is planned in detail. Later phases are outlines and are refined when we reach them.
- Every milestone follows the Definition of Done in TD-010: works (verified by the owner), tests pass, docs updated, committed and pushed.

## Where each refinement lands

| Requirement | Phases |
|---|---|
| 1. Swappable embeddings, model tracking, re-index | 5 (built), 10 (re-index test) |
| 2. Security: validation, limits, access control, safe deletion | 3 (access control, isolation tests), 4 (validation, deletion), 5 (vector deletion), 9, 10 |
| 3. Durable processing, status, retry, no duplicates | 3 (job table), 4 (worker, recovery, retry) |
| 4. RAG evaluation | 5 (retrieval eval), 6 (answer, citation, hallucination eval), 10 (expansion) |
| 5. Single-user now, multi-user later | 3 (user-scoped design), 9 (real auth) |
| 6. Git and GitHub | 1 (setup), every milestone, 11 (public release) |
| 7. Free-plan friendly | Every milestone (TD-011) |
| Collaboration (TD-013) | 1 (collaborator invited after the setup guide), every milestone (branch and pull request workflow) |
| Deployment, Vercel plus separate backend host (TD-014) | 1 (API address from an environment variable), 9 (authentication before any public URL), 11 (deploy) |

---

## Phase 0: Requirement analysis and architecture (COMPLETE)

Delivered: architecture, RAG pipeline design, folder structure, risk list, workflow, refined decisions (`TECHNICAL_DECISIONS.md`), this roadmap, initial `PROJECT_STATE.md`.

## Phase 1: Project initialization and environment setup (CURRENT)

Rule for this phase: one installation or configuration step at a time, each command explained, wait for the owner's confirmation. No software is assumed installed until the owner confirms.

**Progress (2026-11-22):** P1.1 to P1.5 done. P1.6 and P1.7 not started.

| ID | Milestone | Outcome |
|---|---|---|
| P1.1 | Environment audit | Windows, terminal, Git, Python, Node.js and VS Code each checked one at a time, and any missing piece installed |
| P1.2 | Git and GitHub identity | Git configured, GitHub sign-in working, empty private `documind` repository created |
| P1.3 | Repository skeleton and first commit | `.gitignore`, stub `README.md`, `TASKS.md`, `PROJECT_STATE.md` and the decision docs committed and pushed (the `frontend/` and `backend/` folders appear with their first files, because Git does not track empty folders) |
| P1.4 | Backend scaffold | Python 3.12 virtual environment, FastAPI `/health` endpoint, first pytest passing |
| P1.5 | Dependency spike | PyMuPDF and ChromaDB install, import and a real functional check on the owner's machine (retires the Windows install risk). Done: ChromaDB kept, PyMuPDF 1.28.2 pinned (TD-016) |
| P1.6 | Frontend scaffold | Vite, React, TypeScript, Tailwind and Lucide running in the browser |
| P1.7 | Connect and close the phase | Frontend calls backend `/health` using an API address from the `VITE_API_BASE_URL` environment variable (never hardcoded, TD-014), backend allowed origins read from configuration, `SETUP_GUIDE.md` written from the confirmed steps, PyMuPDF licence decision made (TD-017), collaborator invited (TD-013), `PROJECT_STATE.md` updated, tag `phase-1-complete` |

Exit criteria: both servers run on the owner's laptop, the repository is on GitHub, setup is documented, the ChromaDB decision is made (done, TD-016), and the PyMuPDF licence decision is made (TD-017).

## Phase 2: Frontend design and implementation (outline)

The UI is built against a typed mock-data layer that mirrors the planned API shapes, so Phase 3 replaces mocks without rewrites.

- P2.1 Design tokens, light and dark theme, layout shell.
- P2.2 Documents dashboard (cards, status badges, empty state).
- P2.3 Upload UI and processing, failed and retry states.
- P2.4 Chat UI with citation chips (mock data).
- P2.5 Summary, comparison and study screens (skeletons).
- P2.6 Loading, error and empty-state polish.

## Phase 3: Backend architecture and API (outline)

- P3.1 Config, logging and error handling.
- P3.2 Database models, seeded local user, `current_user` dependency (TD-009).
- P3.3 User-scoped repositories and cross-user isolation tests (TD-006).
- P3.4 Documents API and the `processing_jobs` table.
- P3.5 Frontend switches from mocks to the real documents API.

## Phase 4: PDF upload, extraction and processing (outline)

- P4.1 Upload validation, limits and duplicate detection (TD-006).
- P4.2 Job queue, worker, restart recovery and duplicate-job prevention (TD-007), with tests that simulate a restart.
- P4.3 PDF extraction behind an interface (PyMuPDF today, see TD-017), page metadata and scanned-PDF detection.
- P4.4 Page-aware chunker.
- P4.5 Status, progress and retry endpoints plus UI.
- P4.6 Safe deletion job (files and database; vector step added in Phase 5).

## Phase 5: Embeddings, vector database and RAG (outline)

- P5.1 Provider interfaces and `embedding_profiles` (TD-004).
- P5.2 First embedding provider, chosen after a live check of free-tier limits.
- P5.3 `VectorStore` over ChromaDB and the embed stage in the job worker.
- P5.4 Retrieval service.
- P5.5 Re-index job and the `needs_reindex` flow.
- P5.6 Evaluation fixtures and retrieval metrics (TD-008).
- P5.7 Deletion removes vectors (verified).

## Phase 6: Question answering and citations (outline)

- P6.1 LLM provider, chosen after a live limits check.
- P6.2 Query rewriting, prompt and relevance gate.
- P6.3 Citation resolution and validation.
- P6.4 Chat API with history and follow-ups.
- P6.5 Chat UI with PDF viewer jumping to the cited page.
- P6.6 Answer, citation and hallucination evals and the first baseline.

## Phase 7: Summarization (7A) and comparison (7B) (outline)

- 7A: section detection, section-by-section then whole-document summaries with caching, key points and terminology.
- 7B: aligned retrieval across documents, structured comparison report, UI.

## Phase 8: Smart Study Mode (outline)

Multiple-choice questions, flashcards, exam questions and revision notes, generated as validated structured output and cached.

## Phase 9: Database integration, authentication and security (outline)

Swap in real authentication (TD-009), Alembic migrations, rate limiting, PostgreSQL readiness and a security review. Authentication must be complete before any public URL exists. Decide the token-versus-cookie approach with separate frontend and backend domains in mind, and add per-user quotas for the public demo (TD-014).

## Phase 10: Testing, debugging and performance (outline)

Expand evals, test large and malformed PDFs, test re-indexing and restart recovery end to end, review PDF-parser isolation, run a dependency audit.

## Phase 11: Deployment, GitHub documentation and polish (outline)

Nothing is deployed before this phase, and not before Phases 9 and 10 are complete (TD-014).

- P11.1 Secret scan, repository made public (this also makes Vercel collaboration free and unlocks rulesets on GitHub Free). A `LICENSE` file that matches the TD-017 decision is in place.
- P11.2 Choose and set up the backend host after re-checking live pricing: persistent volume, one instance, environment variables, and enough memory and disk for ChromaDB (TD-016).
- P11.3 Deploy the backend, with CORS limited to the frontend domain, then check `/health` and a restart-recovery test.
- P11.4 Deploy the frontend on Vercel (`frontend/` as the root directory, `VITE_API_BASE_URL` set).
- P11.5 Demo guardrails: per-user quotas, upload limits, data notice.
- P11.6 `DEPLOYMENT.md`, README with screenshots and an architecture diagram, final cleanup, and the live URL for both LinkedIn posts.
