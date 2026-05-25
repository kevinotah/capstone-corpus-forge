# Corpus Forge — Project Checklist

> Click checkboxes to track progress. One person per area — coordinate before touching another member's files.

---

## Team

| Member | Role |
|--------|------|
| **Kevin** | Backend & Storage |
| **Cindy** | Frontend & UX |
| **Duc** | DevOps, QA & Integration |

---

## Stage 1 — Foundation

### Kevin — Backend & Storage

- [x] Flask upload endpoint
- [x] List, delete, select endpoints
- [x] Store files on disk
- [x] SQLite metadata persistence
- [x] File size & type validation
- [x] Unit tests for endpoints

### Cindy — Frontend & UX

- [x] Upload UI (Jinja2)
- [x] Document list view
- [x] Select documents for AI
- [x] File preview
- [x] Client-side validation
- [x] Responsive styling

### Duc — DevOps & QA

- [x] Run script / docker-compose
- [x] Env setup instructions
- [ ] Persistence checks (survive server restart)
- [ ] Integration tests (upload → list → delete)
- [ ] Stage-1 acceptance testing
- [ ] Test data set

---

## Stage 2 — AI Features

### Kevin — Backend & Storage

- [ ] Integrate RAG / No-RAG (lab 15)
- [ ] Chat endpoint
- [ ] Flashcard generation endpoint
- [ ] Quiz generation endpoint
- [ ] Code review mode (code files)
- [ ] Token usage tracking
- [ ] Custom prompt / param API

### Cindy — Frontend & UX

- [ ] Chat UI
- [ ] Flashcard view
- [ ] Quiz view
- [ ] Code review view
- [ ] Token usage tab
- [ ] Tone / prompt settings UI

### Duc — DevOps & QA

- [ ] Stage-2 integration tests
- [ ] AI response validation
- [ ] Error handling (empty / corrupt files)
- [ ] Layer 2 feature (team pick)
- [ ] Final end-to-end smoke test

---

## Stage 3 — Polish & Delivery

### Kevin — Backend & Storage

- [ ] Harden validation (edge cases, malformed files)
- [ ] Consistent error responses (JSON error format)
- [ ] API rate limiting / abuse guards
- [ ] Review and clean up all TODO comments
- [ ] Write / update API documentation
- [ ] Confirm all data persists correctly across restarts

### Cindy — Frontend & UX

- [ ] UI consistency pass (spacing, colours, fonts)
- [ ] Loading states on all async actions
- [ ] Empty states (no documents, no results)
- [ ] Error messages visible to user (not just console)
- [ ] Mobile / responsive final check
- [ ] Accessibility pass (labels, tab order, contrast)
- [ ] Write README screenshots / usage examples

### Duc — DevOps & QA

- [ ] Full regression test run (all stages)
- [ ] Test broken / empty / oversized files
- [ ] Test concurrent uploads
- [ ] Verify docker-compose works on a clean machine
- [ ] Write SETUP.md (step-by-step from clone to running)
- [ ] Demo walkthrough script
- [ ] Final sign-off — all Stage 1 & 2 criteria met

---

## Layer 2 — Extra Challenge (team pick one)

- [ ] **RAG-style selective context** — pass only relevant chunks to AI instead of full documents
- [ ] **Prompt engineering** — iteratively improve prompts for a specific task
- [ ] **Interactive visuals** — generate charts / visuals from documents, user can interact
- [ ] **Robustness & testing** — comprehensive error handling, graceful degradation, edge case tests

---

## Dependencies

```
Stage 1 (Kevin: endpoints + DB)
  ↓
Stage 1 (Cindy: connect UI to API)
  ↓
Stage 1 (Duc: integration tests + acceptance)
  ↓
Stage 2 (Kevin: AI endpoints)
  ↓
Stage 2 (Cindy: AI views)
  ↓
Stage 2 (Duc: AI tests + Layer 2)
  ↓
Stage 3 (everyone: polish + delivery)
```

---

## Core Rules

- Pull latest before starting any task
- One person per file — ask before touching someone else's area
- Branches: `backend/...`, `frontend/...`, `devops/...`
- Push + test before marking a task done
- Merge only after another member has reviewed