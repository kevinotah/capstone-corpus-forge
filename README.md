# Corpus Forge

Corpus Forge is a small Python web app for uploading documents, keeping them on disk, selecting which files the AI can use, and generating AI-assisted outputs such as chat answers, flashcards, quizzes, and code reviews.

## What It Has

- Document upload with filename sanitization and size/type checks.
- Persistent storage using SQLite metadata plus files saved under `application/uploads/`.
- Document actions for listing, selecting, previewing, and deleting files.
- AI pages for chat, flashcards, quiz generation, and code review.
- A simple RAG / NoRAG module in `application/rag/`.
- Pytest-based tests under `application/tests/`.

## Project Layout

- `application/app.py` - Flask app and routes.
- `application/config.py` - app settings such as upload limits and allowed extensions.
- `application/storage.py` - document storage and SQLite metadata handling.
- `application/rag/` - AI orchestration, retriever logic, and prompt templates.
- `application/templates/` - Jinja templates for the UI.
- `application/static/` - CSS and other static assets.
- `application/tests/` - pytest test files.
- `application/uploads/` - stored uploaded files.
- `application/data/` - SQLite database files.

## Requirements

- Python 3.11 or newer is recommended.
- `pip`.
- A virtual environment is strongly recommended.
- Optional for AI features:
	- `GOOGLE_API_KEY` for Gemini access.
	- `USE_RAG=true` to switch from the simple full-document path to the RAG path.

## Install

From the project root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install python-dotenv
```

If you want to use the AI features with Gemini, also install:

```bash
pip install google-genai pypdf
```

If you want the RAG path, you will also need the optional retrieval dependencies used by `application/rag/`.

## Run

Start the Flask app from the project root:

```bash
source .venv/bin/activate
python -m flask --app application/app.py run
```

Then open:

```text
http://127.0.0.1:5000
```

## Test

Run the tests with:

```bash
source .venv/bin/activate
pytest -q
```

## Environment Variables

- `SECRET_KEY` - Flask secret key.
- `GOOGLE_API_KEY` - required for Gemini-backed AI calls.
- `USE_RAG=true` - enables the RAG retriever path instead of the simpler no-RAG path.

## Notes

- Uploaded files are saved under `application/uploads/`.
- Metadata is stored in `application/data/metadata.sqlite`.
- The app currently supports document chat, flashcards, quiz generation, and code review pages.
- The UI is intentionally simple so the project stays manageable as a school capstone.


