import json
import os
from pathlib import Path
import numpy as np


STATE_FILENAME = "persist_state.json"


def _state_path() -> Path:
    # place the state file at the repository root (one level above Functions)
    return Path(__file__).resolve().parents[1] / STATE_FILENAME


def _make_serializable(obj):
    # recursively convert numpy types and arrays to native Python types
    if isinstance(obj, dict):
        return {k: _make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_make_serializable(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    # fall back to primitives or str
    try:
        json.dumps(obj)
        return obj
    except Exception:
        return str(obj)


def save_state(state: dict):
    """Save the provided `state` dict to a JSON file.

    The function will convert numpy types to native types so the file is JSON serializable.
    """
    path = _state_path()
    serializable = _make_serializable(state)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)
    except Exception:
        # best-effort: ignore persistence errors to avoid breaking app
        return False
    return True


def load_state() -> dict:
    """Load persisted state. Returns empty dict if no file or on error."""
    path = _state_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def clear_state():
    path = _state_path()
    try:
        if path.exists():
            path.unlink()
            return True
    except Exception:
        return False
    return True
