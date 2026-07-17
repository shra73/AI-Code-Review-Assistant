"""
app/services/analyzer.py

Static analysis service layer.
NEVER executes or imports user-uploaded source code.
Only invokes external CLI analyzers (Pylint, Bandit, Radon).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Final

SUBPROCESS_TIMEOUT: Final[int] = 30


def _validate_file_path(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not path.is_file():
        raise FileNotFoundError(f"Path is not a file: {file_path}")
    return path


def _run_tool(command: list[str], tool_name: str) -> str:
    executable = command[0]

    # Skip which() check for the current Python interpreter
    if executable not in ("python", sys.executable) and shutil.which(executable) is None:
        return f"[{tool_name}] Error: '{executable}' is not installed."

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"[{tool_name}] Analysis timed out after {SUBPROCESS_TIMEOUT} seconds."
    except OSError as exc:
        return f"[{tool_name}] Failed to execute: {exc}"

    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    if stdout and stderr:
        return f"{stdout}\n\n------ STDERR ------\n{stderr}"
    return stdout or stderr or f"[{tool_name}] No output generated."


def run_pylint(file_path: str) -> str:
    try:
        _validate_file_path(file_path)
    except FileNotFoundError as exc:
        return f"[Pylint] {exc}"
    # Use sys.executable so it works inside your venv
    return _run_tool([sys.executable, "-m", "pylint", file_path], "Pylint")


def run_bandit(file_path: str) -> str:
    try:
        _validate_file_path(file_path)
    except FileNotFoundError as exc:
        return f"[Bandit] {exc}"
    return _run_tool([sys.executable, "-m", "bandit", file_path], "Bandit")


def run_radon(file_path: str) -> str:
    try:
        _validate_file_path(file_path)
    except FileNotFoundError as exc:
        return f"[Radon] {exc}"
    return _run_tool([sys.executable, "-m", "radon", "cc", "-s", "-a", file_path], "Radon")


def analyze_file(file_path: str) -> dict[str, str]:
    """Run all static analyzers and return their reports."""
    return {
        "pylint": run_pylint(file_path),
        "bandit": run_bandit(file_path),
        "radon": run_radon(file_path),
    }
