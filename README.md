# DocuMind

**Understand Documents. Discover Intelligence.**

DocuMind is an AI-powered document intelligence platform. Upload PDFs, ask questions and get answers grounded in your documents, with page citations you can click.

> **Status:** early development. Phase 1 (project setup) is complete: the backend and the frontend run on a developer machine and talk to each other. The product features below are **not built yet**. There is no live demo yet (planned for Phase 11).

## Planned features

- Document management: upload, preview, delete, processing status
- AI chat grounded in your documents, with clickable page citations
- Summaries, key points and key terminology
- Multi-document comparison
- Study mode: multiple-choice questions, flashcards, revision notes

## Tech stack

| Layer | Choice | State |
|---|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS, Lucide icons | Set up. The home page shows whether it can reach the backend |
| Backend | Python 3.12, FastAPI | Set up. One endpoint, `GET /health`, with tests |
| PDF reading | PyMuPDF | Installed and checked on Windows |
| Vector database | ChromaDB | Installed and checked on Windows |
| Database | SQLite (PostgreSQL later) | Planned, Phase 3 |
| Embeddings and AI model | Hosted providers, configurable and swappable | Planned, Phases 5 and 6. Providers not chosen yet |

Everything that needs AI runs in the cloud, so DocuMind works on a modest laptop.

## Getting started

Setup for Windows, step by step, is in [SETUP_GUIDE.md](SETUP_GUIDE.md). In short: install Git, Python 3.12 and Node.js, create the backend's virtual environment, run `npm ci` in the frontend, and start the two servers. When both are running, the page at http://localhost:5173/ shows "Backend connected".

macOS and Linux have not been tested yet.

## Project documents

| File | What it is |
|---|---|
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | How to run DocuMind on your computer |
| [PROJECT_STATE.md](PROJECT_STATE.md) | Where the project is right now, what was verified, and the exact next steps |
| [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) | The plan, phase by phase |
| [TASKS.md](TASKS.md) | Who owns which milestone, and the decisions waiting |
| [TECHNICAL_DECISIONS.md](TECHNICAL_DECISIONS.md) | Why things are built the way they are |

## Roadmap

Phase 0 (architecture) and Phase 1 (setup) are done. Next: Phase 2 frontend design, Phase 3 backend API, Phase 4 PDF processing, Phase 5 embeddings and retrieval, Phase 6 questions and citations, Phase 7 summaries and comparison, Phase 8 study mode, Phase 9 database, login and security, Phase 10 testing and performance, Phase 11 deployment and polish. Details are in [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md).

## Contributing

Work happens on a branch and is merged through a pull request, never straight to `main`. The rules are in section 8 of [SETUP_GUIDE.md](SETUP_GUIDE.md) and in [TECHNICAL_DECISIONS.md](TECHNICAL_DECISIONS.md) (TD-010, TD-011 and TD-013).

## Licence

DocuMind is released under the **GNU Affero General Public License v3.0** (AGPL-3.0). The full text is in [LICENSE](LICENSE).

The reason is PyMuPDF, the library that reads the PDFs. It is available under the AGPL-3.0 or a paid commercial licence from Artifex, and DocuMind uses it under the AGPL-3.0 (decision TD-017). In practice, if you run a modified version of DocuMind as a network service, the AGPL requires you to offer its users the source code. Other dependencies keep their own licences. This is a plain-language summary and not legal advice, so read the licence itself for the exact terms.
