import json
from pathlib import Path

from config import DEFAULT_CATEGORIES


# Die Settings-Datei liegt immer neben diesem Skript,
# unabhängig davon, von welchem Ordner aus gestartet wird.
SETTINGS_FILE = Path(__file__).with_name("settings.json")


def _default_settings():
    return {"categories": DEFAULT_CATEGORIES.copy()}


def load_settings():

    if not SETTINGS_FILE.exists():
        return _default_settings()

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            settings = json.load(file)

        if not isinstance(settings, dict):
            raise ValueError("Invalid settings format")

        categories = settings.get("categories")

        if not isinstance(categories, dict) or not categories:
            raise ValueError("Invalid categories")

        for category, extensions in categories.items():
            if not isinstance(category, str) or not isinstance(extensions, list):
                raise ValueError("Invalid category entry")
            if not all(isinstance(item, str) for item in extensions):
                raise ValueError("Invalid extension entry")

        return settings

    except (OSError, json.JSONDecodeError, ValueError):
        return _default_settings()


def save_settings(settings):

    temporary_file = SETTINGS_FILE.with_suffix(".json.tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(
            settings,
            file,
            indent=4,
            ensure_ascii=False
        )

    temporary_file.replace(SETTINGS_FILE)
