"""Logging Service — stores every API request as a JSON line in a log file.

Each line in the log file is a standalone JSON object (JSONL format).
This makes it easy to append new entries without reading the whole file.

Example log file (requests.jsonl):
    {"timestamp": "2026-02-12T14:30:00+00:00", "model": "llama-3.3-70b-versatile", "cost": 0.001}
    {"timestamp": "2026-02-12T14:31:00+00:00", "model": "openai/gpt-oss-20b", "cost": 0.0002}
"""

import json
from datetime import datetime, timezone
from pathlib import Path

# Path to the logs directory and log file (relative to project root)
# __file__ = this file → .parent = backend/ → .parent = project root → / "logs"
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOGS_DIR / "requests.jsonl"


def log_request(data: dict) -> None:
    """Append a request log entry as a JSON line to the log file.

    Args:
        data: Dictionary with the data to log (e.g. model, cost, tokens).
    """
    # Create the logs/ directory if it doesn't exist yet
    LOGS_DIR.mkdir(exist_ok=True)

    # Build the log entry: current timestamp + all data fields merged together
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), **data}

    # Open the file in append mode ("a") so we add to the end, never overwrite
    with LOG_FILE.open("a") as f:
        # Convert dict to JSON string and write as one line
        f.write(json.dumps(entry) + "\n")


def read_logs() -> list[dict]:
    """Read all log entries from the JSONL file.

    Returns:
        List of log entries as dictionaries. Empty list if no logs exist yet.
    """
    # If the log file doesn't exist yet, there's nothing to read
    if not LOG_FILE.exists():
        return []

    # Read the file line by line and parse each line as JSON
    logs = []
    with LOG_FILE.open("r") as f:
        for line in f:
            line = line.strip()          # remove whitespace and newline characters
            if line:                     # skip empty lines
                logs.append(json.loads(line))  # JSON string → Python dict
    return logs


def get_stats() -> dict:
    """Calculate statistics from all logged requests.

    Returns:
        Dictionary with:
        - total_requests: how many requests were made
        - total_cost: sum of all request costs
        - average_cost: average cost per request
        - model_usage: dict counting how often each model was used
    """
    # Read all log entries
    logs = read_logs()

    # If no logs exist yet, return zeroed-out stats
    if not logs:
        return {"total_requests": 0, "total_cost": 0.0, "average_cost": 0.0, "model_usage": {}}

    # Sum up the "actual_cost" field from each log entry
    # .get() returns 0 if the key is missing (defensive programming)
    total_cost = sum(log.get("actual_cost", 0) for log in logs)

    # Count how often each model was used
    model_usage = {}
    for log in logs:
        model = log.get("model")
        if model:
            # .get(model, 0) returns 0 if the model isn't in the dict yet
            model_usage[model] = model_usage.get(model, 0) + 1

    return {
        "total_requests": len(logs),
        "total_cost": round(total_cost, 6),
        "average_cost": round(total_cost / len(logs), 6),
        "model_usage": model_usage,
    }
