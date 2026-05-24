from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, abort, jsonify, redirect, flash, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from application import config as default_config
from application.storage import DocumentStore


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=default_config.SECRET_KEY,
        UPLOAD_FOLDER=str(default_config.UPLOAD_FOLDER),
        DATABASE_PATH=str(default_config.DATABASE_PATH),
        MAX_CONTENT_LENGTH=default_config.MAX_CONTENT_LENGTH,
        ALLOWED_EXTENSIONS=default_config.ALLOWED_EXTENSIONS,
    )
    if test_config is not None:
        app.config.update(test_config)

    store = DocumentStore(Path(app.config["UPLOAD_FOLDER"]).parent, app.config["DATABASE_PATH"])

    def allowed_file(file_name: str) -> bool:
        if "." not in file_name:
            return False
        extension = file_name.rsplit(".", 1)[1].lower()
        return extension in app.config["ALLOWED_EXTENSIONS"]

    @app.post("/upload")
    def upload_document():
        uploaded_file = request.files.get("file")
        if uploaded_file is None or uploaded_file.filename == "":
            flash("No file selected for upload.")
            return redirect(url_for("index"))

        file_name = uploaded_file.filename or ""
        safe_name = secure_filename(file_name)
        if not safe_name:
            flash("Invalid filename.")
            return redirect(url_for("index"))

        if not allowed_file(safe_name):
            flash(f"Unsupported file type: {file_name}")
            return redirect(url_for("index"))

        try:
            doc = store.save_document(safe_name, uploaded_file.read())
            flash(f"Uploaded {doc['name']}")
        except Exception as exc:
            flash(f"Failed to save file: {exc}")

        return redirect(url_for("index"))

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        max_bytes = app.config.get("MAX_CONTENT_LENGTH")
        try:
            max_mb = f"{max_bytes // (1024*1024)} MB"
        except Exception:
            max_mb = str(max_bytes)
        flash(f"Uploaded file is too large (max: {max_mb}).")
        return redirect(url_for("index"))

    @app.get("/documents")
    def documents():
        return jsonify(store.list_documents()), 200

    @app.get("/documents/<document_id>/raw")
    def raw_document(document_id: str):
        document = next((doc for doc in store.list_documents() if doc["id"] == document_id), None)
        if document is None:
            abort(404)

        path = Path(document["path"])
        if not path.exists():
            abort(404)

        return send_file(path, mimetype=document["mime"], as_attachment=False, download_name=document["name"])

    @app.get("/documents/<document_id>/preview")
    def preview_document(document_id: str):
        document = next((doc for doc in store.list_documents() if doc["id"] == document_id), None)
        if document is None:
            flash("Document not found.")
            return redirect(url_for("index"))

        path = Path(document["path"])
        if not path.exists():
            flash("Document file is missing on disk.")
            return redirect(url_for("index"))

        is_image = document["mime"].startswith("image/")
        text_preview = None
        if document["mime"].startswith("text/") or document["name"].lower().endswith((".txt", ".md")):
            try:
                text_preview = path.read_text(encoding="utf-8", errors="replace")[:12000]
            except OSError:
                text_preview = "Preview unavailable for this file."

        return render_template(
            "preview.html",
            document=document,
            is_image=is_image,
            text_preview=text_preview,
        )

    @app.post("/documents/<document_id>/delete")
    def delete_document(document_id: str):
        store.delete_document(document_id)
        return redirect(url_for("index"))

    @app.post("/documents/<document_id>/select")
    def select_document(document_id: str):
        selected_value = request.form.get("selected", "0")
        selected = selected_value in {"1", "true", "True", "on", "yes"}
        store.select_document(document_id, selected)
        return redirect(url_for("index"))

    @app.get("/")
    def index() -> str:
        documents = store.list_documents()
        return render_template(
            "index.html",
            documents=documents,
            allowed_extensions=sorted(app.config["ALLOWED_EXTENSIONS"]),
            max_content_length=app.config["MAX_CONTENT_LENGTH"],
        )

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)