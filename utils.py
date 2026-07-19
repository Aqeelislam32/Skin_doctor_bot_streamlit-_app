import os


def ensure_uploads_dir(path: str = "uploads") -> str:
    """Make sure the uploads folder exists, create it if not."""
    os.makedirs(path, exist_ok=True)
    return path
