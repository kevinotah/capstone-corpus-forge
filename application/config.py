from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SECRET_KEY = "maximum-effort"
UPLOAD_FOLDER = BASE_DIR / "uploads"
DATABASE_PATH = BASE_DIR / "data" / "metadata.sqlite"
MAX_CONTENT_LENGTH = 20 * 1024 * 1024
ALLOWED_EXTENSIONS = {"txt", "pdf", "doc", "docx", "md", "png", "jpg", "jpeg"}