from pathlib import Path


def load_text_file(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    return file_path.read_text(encoding="utf-8")


def load_sql_file(file_path: Path) -> str:
    return load_text_file(file_path)
