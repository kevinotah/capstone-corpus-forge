from flask import Flask, render_template


def create_app() -> Flask:
    app = Flask(__name__)

    # TODO: configure secret key, upload directory, and database path.
    # TODO: register document management routes for upload, list, select, and delete.

    @app.get("/")
    def index() -> str:
        # TODO: load documents from local persistence and pass them to the template.
        documents = []
        return render_template("index.html", documents=documents)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True)
