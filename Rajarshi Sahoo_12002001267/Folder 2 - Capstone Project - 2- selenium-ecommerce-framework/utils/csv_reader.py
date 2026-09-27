"""CSV data helpers used by automated tests."""

import csv
from pathlib import Path


def read_csv(file_path: str | Path) -> list[dict[str, str]]:
    """Return CSV rows as dictionaries keyed by the header names."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


def read_csv_as_tuples(file_path: str | Path) -> list[tuple[str, ...]]:
    """Return CSV rows as tuples containing values in header order."""
    rows = read_csv(file_path)
    return [tuple(row.values()) for row in rows]
