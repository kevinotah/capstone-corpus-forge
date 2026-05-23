from __future__ import annotations

import mimetypes
import os
import re
import sqlite3
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class DocumentStore:
    """Simple document store handling filesystem writes and SQLite metadata.

    Responsibilities:
    - Store uploaded file bytes under `uploads/` using a UUID-prefixed sanitized filename.
    - Persist metadata in an SQLite database under `data/metadata.sqlite`.
    - Perform atomic writes and cleanup on failure to avoid orphan files.
    """

    def __init__(self, root_path: str | Path, database_path: str | Path | None = None) -> None:
        self.root_path = Path(root_path)
        self.uploads_path = self.root_path / "uploads"
        self.data_path = self.root_path / "data"
        self.database_path = Path(database_path) if database_path is not None else self.data_path / "metadata.sqlite"

        self.uploads_path.mkdir(parents=True, exist_ok=True)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_database()

    def list_documents(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT id, name, path, size, mime, uploaded_at, selected
                FROM documents
                ORDER BY uploaded_at DESC, name ASC
                """
            ).fetchall()

        return [self._row_to_document(row) for row in rows]

    def save_document(self, file_name: str, content: bytes) -> dict[str, Any]:
        document_id = str(uuid.uuid4())

        # sanitize filename: keep alphanumerics, dot, dash, underscore; collapse others to '_'
        orig_name = Path(file_name).name
        name = re.sub(r"[^\w.\-]+", "_", orig_name, flags=re.UNICODE).strip("_ ")
        if not name or name.startswith("."):
            name = "file"

        # limit base length to avoid filesystem limits
        base, ext = os.path.splitext(name)
        base = base[:200]
        safe_name = f"{base}{ext.lower()}"

        stored_name = f"{document_id}-{safe_name}"
        stored_path = self.uploads_path / stored_name

        # atomic write to temporary file in same directory
        tmp_fd, tmp_path_str = tempfile.mkstemp(prefix=".", dir=str(self.uploads_path))
        try:
            with os.fdopen(tmp_fd, "wb") as tmp_file:
                tmp_file.write(content)
                tmp_file.flush()
                os.fsync(tmp_file.fileno())

            # atomic move into final destination
            os.replace(tmp_path_str, str(stored_path))

            uploaded_at = datetime.now(timezone.utc).isoformat()
            mime_type = mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
            size = len(content)

            document = {
                "id": document_id,
                "name": safe_name,
                "path": str(stored_path),
                "size": size,
                "mime": mime_type,
                "uploaded_at": uploaded_at,
                "selected": 0,
            }

            # insert metadata; if this fails, remove the stored file to avoid orphaned files
            try:
                with self._connect() as connection:
                    connection.execute(
                        """
                        INSERT INTO documents (id, name, path, size, mime, uploaded_at, selected)
                        VALUES (:id, :name, :path, :size, :mime, :uploaded_at, :selected)
                        """,
                        document,
                    )
                    connection.commit()
            except Exception:
                # cleanup file on DB failure
                try:
                    if stored_path.exists():
                        stored_path.unlink()
                finally:
                    raise

            return document
        finally:
            # ensure temp file removed if something went wrong before replace
            if os.path.exists(tmp_path_str):
                try:
                    os.remove(tmp_path_str)
                except Exception:
                    pass

    def delete_document(self, document_id: str) -> None:
        document = self._get_document(document_id)
        if document is None:
            return

        stored_path = Path(document["path"])
        if stored_path.exists():
            stored_path.unlink()

        with self._connect() as connection:
            connection.execute("DELETE FROM documents WHERE id = ?", (document_id,))
            connection.commit()

    def select_document(self, document_id: str, selected: bool) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE documents SET selected = ? WHERE id = ?",
                (1 if selected else 0, document_id),
            )
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    mime TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL,
                    selected INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            connection.commit()

    def _get_document(self, document_id: str) -> sqlite3.Row | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, name, path, size, mime, uploaded_at, selected FROM documents WHERE id = ?",
                (document_id,),
            ).fetchone()
        return row

    @staticmethod
    def _row_to_document(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "name": row["name"],
            "path": row["path"],
            "size": row["size"],
            "mime": row["mime"],
            "uploaded_at": row["uploaded_at"],
            "selected": bool(row["selected"]),
        }
