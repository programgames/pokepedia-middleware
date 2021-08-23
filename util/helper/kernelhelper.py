from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def get_csv_path() -> str:
    return str(Path(__file__).parent.parent)