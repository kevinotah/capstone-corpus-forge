# Corpus Forge — Implementation Plan (Team of 3)

> Source: synthesized from repository docs and briefs: "Capstone Project - Kick-Off" and "Project Corpuse Forge - Executive Summary", plus repository context (templates, agents, journaling hooks).

## Project Summary (assumptions)
- Objective: build "Corpus Forge": a collaborative web platform to create, curate, store, and export text/audio corpora for NLP experiments. (If actual product goals differ, we will adapt in Week 0.)
- Primary users: researchers, instructors, students who need to assemble labelled corpora and export datasets.
- Key non-functional needs: reproducibility, versioned datasets, lightweight UI, team collaboration, and straightforward import/export (CSV/JSON/CoNLL etc.).

## Success Criteria (MVP)
- Users can create a project and upload raw text files.
- Users can annotate items (labels/tags) or upload annotations in a standard format.
- Projects are versioned and downloadable as a dataset (CSV/JSON) with metadata.
- Basic user interface with authentication (team-sharing optional), automated tests, and CI for builds.

## Proposed Tech Stack (recommended)
- Backend: Python + FastAPI (async, lightweight) or Node.js + Express. (Pick one; this plan assumes Python/FastAPI.)
- Database: PostgreSQL (for datasets and metadata) or SQLite for prototype; use SQLAlchemy/Databases.
- Frontend: React (Vite) with TypeScript, or a simple server-rendered UI if team prefers minimal JS.
- Storage: local filesystem for prototype; S3-compatible (minio) for production.
- Dev tooling: Docker for local dev, GitHub Actions for CI, pytest, ESLint/Prettier.

## High-level Architecture
- REST API (CRUD for projects, documents, annotations, exports).
- Web UI (project dashboard, upload/annotate/export flows).
- Worker (background export/versioning tasks) — optional; can be synchronous for MVP.
- Storage layer with metadata in DB and raw files on disk.

## Team Roles & Suggested Division of Labour (3 members)
- Team members: Kevin (Backend Lead), Cindy (Frontend Lead), Duc (DevOps / Data & QA Lead)

- Kevin — Backend Lead (API, DB, auth, export pipeline)
  - Design DB schema, implement API endpoints, authentication, validation, export routines, unit tests for backend.
- Cindy — Frontend Lead (UX, annotation UI, upload flows)
  - Build React UI, integrate with API, implement annotation components, client-side validation, accessibility basics, e2e tests (optional).
- Duc — DevOps / Data & QA Lead (infrastructure, CI, docs, testing, sample data)
  - Dockerize services, create GitHub Actions CI, set up DB migrations, create seed/sample corpora, integration tests, CI test runs, documentation, release notes.


## Two-week Plan (tight deadline)

Given the 2-week constraint, the scope is reduced to a minimal, demonstrable MVP focused on core flows: create project, upload documents, annotate simple labels, and export a dataset.

Week 0 (Kickoff — Day 1)
- Tasks:
  - Align on exact MVP features and acceptance criteria (30–60 min).
  - Agree tech choices: use Python + FastAPI (backend), React (frontend) or fallback to simple server-rendered pages to save time.
  - Create three GitHub issues for the top-priority tasks and assign to Kevin, Cindy, Duc.
  - Prepare a minimal Docker Compose file or run instructions so reviewers can run the app locally.
- Deliverables: finalized MVP, three assigned issues, and an executable dev run command.

Week 1 (Implementation — Days 2–9)
- Primary goals: backend endpoints for project + upload + export; frontend upload and basic annotation UI.
- Kevin (Backend):
  - Implement minimal FastAPI app with endpoints: POST /projects, POST /projects/{id}/documents (file upload), GET /projects/{id}/export (CSV/JSON).
  - Use SQLite for quick setup; include a simple migration or schema-init script.
  - Add basic unit tests for upload and export.
- Cindy (Frontend):
  - Scaffold a minimal React page or simple HTML form to create a project and upload files to the backend.
  - Implement a very small annotation UI (select a document, choose labels from a fixed list, save annotations).
  - Connect upload and annotation flows to the backend.
- Duc (DevOps / QA):
  - Provide a `docker-compose.yml` or clear run instructions and ensure the app can be started locally by graders.
  - Create sample seed data and a simple automated script to demonstrate upload → annotate → export flow.

Week 2 (Polish & Deliverables — Days 10–14)
- Tasks:
  - Finalize export format and ensure metadata is included.
  - Fix critical bugs, write brief README run instructions, and capture screenshots for the demo.
  - Prepare `REPORT.md` entries (design decisions, AI use, who did what) and a short demo script.
- Deliverables: working MVP for demo, README with run steps, `REPORT.md` draft, and a short demo recording or script.

Notes on priorities: if any task slips, prioritize backend upload+export and a minimal frontend upload form; annotation UI can be the simplest label selector rather than span-based annotation.

## Task Breakdown (detailed, actionable)
- Repo & project setup (Week 0)
  - Create `src/backend/`, `src/frontend/`, `docker/`, `docs/`, `tests/` directories.
  - Add `README.md`, `CONTRIBUTING.md`, PR and issue templates.
  - Create `plan.md` (this file).
- Backend tasks (Kevin):
  - `API`: minimal endpoints: POST /projects, POST /projects/{id}/documents, GET /projects/{id}/export
  - `DB`: simple SQLite schema and init script to keep setup fast.
  - `Export`: implement CSV/JSON serializer with basic metadata.
  - Tests: short unit tests covering upload and export flows.
- Frontend tasks (Cindy):
  - `UI`: minimal project creation and upload form, simple annotation label selector, export trigger.
  - `Integration`: connect directly to backend upload/export endpoints; no complex auth for MVP.
  - `UX`: keep interactions simple and mobile-friendly; prioritize clarity over features.
- DevOps & QA (Duc):
  - `Docker`: provide a `docker-compose.yml` or simple run commands to start the stack.
  - `CI`: add a minimal GitHub Actions workflow to run tests if time allows.
  - `Testing`: create a seed script and a short demo script to validate the flow.
  - `Docs`: write concise README run instructions and verify reproducibility.

## Acceptance Criteria (per feature)
- Upload: user uploads a file ≤ 100MB → server returns item id and preview in UI.
- Annotation: user saves annotation → GET returns consistent annotation payload.
- Export: exported archive includes data + metadata JSON and matches schema in docs.
- CI: PRs must pass linting and test suites before merge.

## Repo Structure Suggestion
- `README.md` — project overview and quickstart
- `plan.md` — this plan
- `src/backend/` — FastAPI app, models, migrations
- `src/frontend/` — React app
- `docker/` — compose files
- `tests/` — unit and integration tests
- `docs/` — design docs, API spec, data schema, `REPORT.md` finalization

## Communication & Workflow
- Branching: feature branches, PRs to `main`. Require 1 approving review + passing CI.
- PR size: keep PRs small (≤ 200 LOC) and focused.
- Meetings: 30-min sync twice weekly; retros every sprint.
- Task tracking: use GitHub issues and projects; label by `backend`/`frontend`/`devops`.

## Risk Mitigation
- If DB setup slows progress, start with SQLite to build end-to-end flows, then migrate to Postgres.
- If annotation UI is complex, implement a simple label/tag UI for MVP and iterate.
- Reserve 10–15% of sprint capacity for integration, bug fixes, and docs.

## Deliverables & Demonstrations
- Mid-term demo (end of Week 1): upload files, annotate a few items, and perform an export.
- Final demo (end of Week 2): working MVP with README and `REPORT.md` draft; show upload → annotate → export flow.

## Suggested Milestones for PRs and Reviews
- Week 0 PR: repo skeleton, `plan.md` update, and run instructions.
- Week 1 PR: backend upload/export endpoints + minimal frontend upload form.
- Week 2 PR: annotation UI, export finalization, README, and `REPORT.md` draft.

## Next Immediate Actions (first 7 days)
1. Run a 30–60 minute kickoff meeting: confirm MVP, pick final stack, and assign owners.
2. Kevin: initialize backend skeleton and provide an OpenAPI stub and schema-init script.
3. Cindy: scaffold a minimal frontend upload form and wire it to the OpenAPI stub.
4. Duc: add `docker-compose.yml` or clear run commands and create sample seed data.
5. Create GitHub issues for the above and assign owners; aim to have the Week 1 PR open by Day 5.

## Notes & Assumptions
- The plan assumes no strict pre-existing product constraints beyond repository docs. If the PDFs specify different scope, update the plan in Week 0.
- Prioritize reproducibility and clear documentation so graders can run the project locally.

---

Prepared by the team plan generator. Update `plan.md` as decisions are finalized.
