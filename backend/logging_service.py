"""Schritt 7: Logging Service.

Hier speicherst du jede API-Anfrage in einer JSONL-Datei (JSON Lines).
Jede Zeile in der Datei ist ein eigenstaendiges JSON-Objekt.

Lernziele:
- Dateien schreiben und lesen mit pathlib
- JSON serialisieren/deserialisieren
- JSONL Format (eine JSON-Zeile pro Eintrag)
- datetime fuer Zeitstempel

Beispiel JSONL:
  {"timestamp": "2024-01-15T10:30:00+00:00", "model": "llama-3.3-70b", "cost": 0.001}
  {"timestamp": "2024-01-15T10:31:00+00:00", "model": "gemma2-9b", "cost": 0.0002}
"""

import json
from datetime import datetime, timezone
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOGS_DIR / "requests.jsonl"


def log_request(data: dict) -> None:
    """Speichere einen Request-Log-Eintrag als JSON-Zeile.

    TODO:
    1. Stelle sicher dass LOGS_DIR existiert: LOGS_DIR.mkdir(exist_ok=True)
    2. Erstelle den Log-Eintrag als Dictionary:
       - "timestamp": aktueller Zeitpunkt als ISO-String
         -> datetime.now(timezone.utc).isoformat()
       - Plus alle Key-Value-Paare aus dem data Dictionary
         -> Tipp: {**dict1, **dict2} merged zwei Dicts
    3. Oeffne LOG_FILE im Append-Modus ("a") und schreibe:
       -> json.dumps(entry) + "\\n"

    Args:
        data: Dictionary mit den zu loggenden Daten.
    """
    pass


def read_logs() -> list[dict]:
    """Lese alle Log-Eintraege aus der JSONL-Datei.

    TODO:
    1. Pruefe ob LOG_FILE existiert -> wenn nicht, return leere Liste
    2. Oeffne die Datei und lese Zeile fuer Zeile
    3. Fuer jede nicht-leere Zeile: json.loads() und zur Liste hinzufuegen
    4. Return die Liste

    Returns:
        Liste von Log-Eintraegen als Dictionaries.
    """
    pass


def get_stats() -> dict:
    """Berechne Statistiken aus den Logs.

    TODO:
    1. Hole alle Logs mit read_logs()
    2. Wenn keine Logs vorhanden, return:
       {"total_requests": 0, "total_cost": 0.0, "average_cost": 0.0, "model_usage": {}}
    3. Berechne:
       - total_cost: Summe aller "actual_cost" Werte
       - model_usage: Dictionary das zaehlt wie oft jedes Modell verwendet wurde
         -> Iteriere ueber logs, fuer jeden Eintrag: model_usage[model] += 1
    4. Return:
       {
           "total_requests": len(logs),
           "total_cost": round(total_cost, 6),
           "average_cost": round(total_cost / len(logs), 6),
           "model_usage": model_usage,
       }

    Returns:
        Dictionary mit Statistiken.
    """
    pass
