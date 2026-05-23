from __future__ import annotations

import io
from pathlib import Path

from application.app import create_app


def _make_test_app(tmp_path: Path):
    upload_folder = tmp_path / "uploads"
    database_path = tmp_path / "data" / "metadata.sqlite"
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret-key",
            "UPLOAD_FOLDER": str(upload_folder),
            "DATABASE_PATH": str(database_path),
        }
    )


def test_upload_list_select_and_delete(tmp_path: Path) -> None:
    app = _make_test_app(tmp_path)
    client = app.test_client()

    upload_response = client.post(
        "/upload",
        data={"file": (io.BytesIO(b"hello world"), "sample.txt")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert upload_response.status_code == 200
    assert b"sample.txt" in upload_response.data

    documents_response = client.get("/documents")
    assert documents_response.status_code == 200

    documents = documents_response.get_json()
    assert len(documents) == 1

    document = documents[0]
    assert document["name"] == "sample.txt"
    assert document["size"] == 11
    assert document["selected"] is False

    stored_file = Path(document["path"])
    assert stored_file.exists()

    select_response = client.post(
        f"/documents/{document['id']}/select",
        data={"selected": "1"},
        follow_redirects=True,
    )
    assert select_response.status_code == 200

    selected_documents = client.get("/documents").get_json()
    assert selected_documents[0]["selected"] is True

    delete_response = client.post(f"/documents/{document['id']}/delete", follow_redirects=True)
    assert delete_response.status_code == 200
    assert b"No documents yet." in delete_response.data

    assert client.get("/documents").get_json() == []
    assert not stored_file.exists()


def test_upload_without_file_keeps_page_working(tmp_path: Path) -> None:
    app = _make_test_app(tmp_path)
    client = app.test_client()

    response = client.post("/upload", data={}, follow_redirects=True)

    assert response.status_code == 200
    assert b"No documents yet." in response.data
    assert client.get("/documents").get_json() == []


def test_upload_rejects_unsupported_extension(tmp_path: Path) -> None:
    app = _make_test_app(tmp_path)
    client = app.test_client()

    response = client.post(
        "/upload",
        data={"file": (io.BytesIO(b"fake video data"), "movie.mp4")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"No documents yet." in response.data
    assert client.get("/documents").get_json() == []


def test_upload_rejects_files_over_20mb(tmp_path: Path) -> None:
    app = _make_test_app(tmp_path)
    client = app.test_client()

    oversized_payload = b"x" * ((20 * 1024 * 1024) + 1)
    response = client.post(
        "/upload",
        data={"file": (io.BytesIO(oversized_payload), "huge.pdf")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    # app now flashes a friendly message and redirects to index on oversized uploads
    assert response.status_code == 200
    assert b"too large" in response.data.lower()
    assert client.get("/documents").get_json() == []