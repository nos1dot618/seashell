from pathlib import Path


def get_file_directory(filepath: str) -> str | None:
    directory = Path(filepath).parent
    return str(directory) if directory.exists() and directory.is_dir() else None


def get_resolved_path(path: str, wd: str) -> str | None:
    path_obj = Path(path)
    if not path_obj.is_absolute():
        path_obj = Path(wd) / path_obj
    path_obj = path_obj.resolve()
    return str(path_obj) if path_obj.exists() else None
