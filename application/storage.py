from pathlib import Path
from typing import Any


class DocumentStore:
    def __init__(self, root_path: str | Path) -> None:
        self.root_path = Path(root_path)
        # TODO: create or load the local persistence layout here.

    def list_documents(self) -> list[dict[str, Any]]:
        # TODO: return saved documents and metadata.
        return []

    def save_document(self, file_name: str, content: bytes) -> dict[str, Any]:
        # TODO: store the file on disk and persist metadata.
        raise NotImplementedError

    def delete_document(self, document_id: str) -> None:
        # TODO: remove the file and metadata only when the user requests it.
        raise NotImplementedError

    def select_document(self, document_id: str, selected: bool) -> None:
        # TODO: persist the AI-selection flag for a document.
        raise NotImplementedError
