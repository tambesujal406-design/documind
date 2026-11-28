# DocuMind: Tasks

Last updated: 2026-11-27

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
| P1.7a | Connect frontend to backend (settings, CORS, `VITE_API_BASE_URL`, status badge) | Sujal | Done |
| P1.7b | Close Phase 1: clean-install rehearsal, `SETUP_GUIDE.md`, lint plan, PyMuPDF licence decision (AGPL-3.0) and `LICENSE`, README | Sujal | Done |
| P1.7c | After the P1.7b merge: collaborator invited and accepted; repository found public and kept public, so history checked for secrets, secret scanning, push protection and dependency alerts confirmed or switched on, ruleset "Protect main" added and tested (TD-020); tag `phase-1-complete` | Sujal | Done |

## Decisions waiting

| Decision | Needed by | Reference |
|---|---|---|
| Run lint, build and tests automatically on GitHub for every pull request (GitHub Actions). Proposed. It also gets around Oxlint being blocked by Windows Smart App Control on the owner's laptop | Before the collaborator's first pull request, or early in Phase 2 | TD-018 |
| Embedding provider | Phase 5 | TD-012 |
| LLM provider | Phase 6 | TD-012 |
| Token vs cookie authentication across separate domains | Phase 9 | TD-014 |
| Backend host and Vercel plan (the repository is already public) | Phase 11 | TD-014 |

## Open actions

| Action | Who | By | Reference |
|---|---|---|---|
| Enable two-factor authentication on the GitHub account (GitHub shows a banner: required before 2027-01-08, or the account is restricted) | Owner, and the collaborator if they see the same banner | 2027-01-08 | TD-020 |
| Follow `SETUP_GUIDE.md` on your own computer and report every step that fails (the first test of a fresh clone on a second computer) | Collaborator | Before the first pull request | `SETUP_GUIDE.md` |
| Raise Required approvals on `main` from 0 to 1, so each person reviews the other's pull requests | Both agree | After the collaborator's first pull request | TD-020 |
| Optional extras: private vulnerability reporting, malware alerts, CodeQL scanning | Owner | Before Phase 11 | TD-020 |

## Later phases

Milestones for Phases 2 to 11 are listed in `DEVELOPMENT_ROADMAP.md` and are copied into this file when each phase starts.
