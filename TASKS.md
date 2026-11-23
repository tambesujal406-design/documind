# DocuMind: Tasks

Last updated: 2026-11-23

Shared task tracker (see TD-013 in `TECHNICAL_DECISIONS.md`). Before starting a milestone, put your name in the Owner column inside your pull request. One milestone has one owner. Status is Todo, In progress or Done.

The full plan for every phase is in `DEVELOPMENT_ROADMAP.md`. The current state of the project is in `PROJECT_STATE.md`.

## Phase 1: Project initialization and environment setup

| ID | Milestone | Owner | Status |
|---|---|---|---|
| P1.1 | Environment audit | Sujal | Done |
| P1.2 | Git and GitHub identity | Sujal | Done |
| P1.3 | Repository skeleton and first commit | Sujal | Done |
| P1.4 | Backend scaffold (virtual environment, `/health`, first pytest) | Sujal | Done |
| P1.5 | Dependency spike (PyMuPDF, ChromaDB) | Sujal | Done |
| P1.6 | Frontend scaffold (Vite, React, TypeScript, Tailwind, Lucide) | Sujal | Done |
| P1.7 | Connect frontend to backend, `SETUP_GUIDE.md`, PyMuPDF licence decision, invite collaborator, tag `phase-1-complete` | Sujal | Todo |

## Decisions waiting

| Decision | Needed by | Reference |
|---|---|---|
| PyMuPDF licence: keep it with an AGPL-3.0 repository, or switch to a permissive PDF library | Before the collaborator is invited (P1.7) | TD-017 |
| Embedding provider | Phase 5 | TD-012 |
| LLM provider | Phase 6 | TD-012 |
| Token vs cookie authentication across separate domains | Phase 9 | TD-014 |
| Backend host and Vercel plan (or public repository) | Phase 11 | TD-014 |

## Later phases

Milestones for Phases 2 to 11 are listed in `DEVELOPMENT_ROADMAP.md` and are copied into this file when each phase starts.
