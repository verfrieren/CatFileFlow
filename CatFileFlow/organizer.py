import shutil
from pathlib import Path

from config import DEFAULT_CATEGORIES
from settings import load_settings


def get_categories():
    """
    Liefert die Kategorien aus settings.json.
    Fallback: die Standardkategorien aus config.py.
    """

    categories = load_settings().get("categories")

    if not isinstance(categories, dict) or not categories:
        return DEFAULT_CATEGORIES

    normalized = {}

    for category, extensions in categories.items():

        if not isinstance(category, str) or not isinstance(extensions, list):
            continue

        normalized[category] = [
            extension if extension.startswith(".") else f".{extension}"
            for extension in extensions
            if isinstance(extension, str)
        ]

    if not normalized:
        return DEFAULT_CATEGORIES

    return normalized


def get_category(file_path, categories=None):

    if categories is None:
        categories = get_categories()

    extension = file_path.suffix.lower()

    for category, extensions in categories.items():
        if extension in extensions:
            return category

    return "Others"


def is_organizable(file_path):
    """
    Nur normale, sichtbare Dateien im obersten Ordner werden sortiert.
    Versteckte Dateien (z.B. .gitignore) und Unterordner bleiben unangetastet.
    """

    return file_path.is_file() and not file_path.name.startswith(".")


def scan_folder(folder_path, categories=None):
    """Listet alle zu sortierenden Dateien auf (ohne etwas zu verschieben)."""

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Invalid folder: {folder_path}")

    if categories is None:
        categories = get_categories()

    results = []

    for file_path in sorted(folder.iterdir()):

        if not is_organizable(file_path):
            continue

        results.append({
            "name": file_path.name,
            "category": get_category(file_path, categories),
            "path": str(file_path)
        })

    return results


def get_unique_path(destination, reserved=()):
    """
    Findet einen freien Dateinamen,
    falls die Datei bereits existiert.
    """

    reserved = set(reserved)
    candidate = destination
    counter = 1

    while candidate.exists() or candidate in reserved:
        candidate = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        counter += 1

    return candidate


def build_plan(folder_path, categories=None):
    """
    Berechnet, wohin jede Datei wandern würde,
    ohne eine einzige Datei anzufassen.

    Das Ergebnis ist identisch mit einer echten Ausführung,
    weil Namenskonflikte schon in der Vorschau berücksichtigt werden.
    """

    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Invalid folder: {folder_path}")

    if categories is None:
        categories = get_categories()

    plan = []
    reserved = set()

    for file_path in sorted(folder.iterdir()):

        if not is_organizable(file_path):
            continue

        category = get_category(file_path, categories)
        target_folder = folder / category
        destination = get_unique_path(
            target_folder / file_path.name,
            reserved
        )
        reserved.add(destination)

        plan.append({
            "name": file_path.name,
            "category": category,
            "source": str(file_path),
            "destination": str(destination),
            "status": "Preview"
        })

    return plan


def organize_folder(folder_path, dry_run=True):
    """
    Sortiert Dateien nach Kategorien.

    dry_run=True:
        Zeigt nur an, was passieren würde.

    dry_run=False:
        Verschiebt die Dateien tatsächlich.
    """

    plan = build_plan(folder_path)

    if dry_run:
        return plan

    for item in plan:

        source = Path(item["source"])
        destination = Path(item["destination"])

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(
                str(source),
                str(destination)
            )

            item["status"] = "Moved"

        except OSError as error:
            # Eine fehlerhafte Datei stoppt nicht das ganze Sortieren.
            item["status"] = "Error: " + " ".join(str(error).split())

    return plan
