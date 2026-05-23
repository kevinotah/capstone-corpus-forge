from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

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
            return redirect(url_for("index"))

        file_name = uploaded_file.filename or ""
        safe_name = secure_filename(file_name)
        if not safe_name or not allowed_file(safe_name):
            return redirect(url_for("index"))

        store.save_document(safe_name, uploaded_file.read())
        return redirect(url_for("index"))

    @app.get("/documents")
    def documents():
        return jsonify(store.list_documents()), 200

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
        return render_template("index.html", documents=documents)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
