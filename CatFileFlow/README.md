# /ᐠ˵- ⩊ -˵マ CatFileFlow

Ein GUI-Tool, das Dateien in einem gewählten Ordner automatisch
nach Kategorien (Bilder, Dokumente, Videos, Musik, Archive, Programme, Sonstiges)
sortiert.

## Voraussetzungen

- Python 3.13+
- requirements.txt installieren:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Starten

```powershell
.\.venv\Scripts\python.exe main.py
```

## Ablauf

1. **Choose Folder** – Ordner auswählen (nur direkte Dateien im Ordner werden sortiert, Unterordner und versteckte Dateien bleiben unangetastet).
2. **Preview Sorting** – zeigt, wohin jede Datei wandern. Es wird nichts verändert.
3. **Start Sorting** – verschiebt die Dateien.
   Bereits vorhandene Dateien werden automatisch umbenannt (`name_1.ext`, `name_2.ext`, …).
   Einzelne Fehler (z.B. gesperrte Dateien) stoppen das Sortieren nicht.

## Eigene Kategorien

Beim ersten Start wird die Datei `settings.json` neben `main.py` angelegt.
Dort kannst du Kategorien und Dateiendungen anpassen:

```json
{
    "categories": {
        "Code": [".py", ".js", ".html"],
        "Images": [".jpg", ".png"]
    }
}
```

Ist die Datei leer, beschädigt oder ungültig, greifen automatisch die
Einstellungen aus `config.py`!!
