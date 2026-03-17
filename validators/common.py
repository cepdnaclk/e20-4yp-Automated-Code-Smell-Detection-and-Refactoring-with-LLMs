import re
import subprocess
import tempfile
from pathlib import Path

from models.schemas import ValidationStatus
from validators.python_validator import validate_python

PUBLIC_JAVA_TYPE_RE = re.compile(r"public\s+(?:class|interface|enum|record)\s+([A-Za-z_][A-Za-z0-9_]*)")
JAVA_CODE_BLOCK_RE = re.compile(r"```(?:java)?\n(.*?)```", re.DOTALL | re.IGNORECASE)
JAVA_START_RE = re.compile(r"\b(public\s+(?:class|interface|enum|record)|class\s+[A-Za-z_])")
PYTHON_CODE_BLOCK_RE = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL | re.IGNORECASE)
PYTHON_START_RE = re.compile(r"^(def |class |from |import )", re.MULTILINE)


def _sanitize_java_code(code: str) -> str:
    text = (code or "").strip()
    block_match = JAVA_CODE_BLOCK_RE.search(text)
    if block_match:
        return block_match.group(1).strip()
    start_match = JAVA_START_RE.search(text)
    if start_match:
        return text[start_match.start():].strip()
    return text


def _sanitize_python_code(code: str) -> str:
    text = (code or "").strip()
    block_match = PYTHON_CODE_BLOCK_RE.search(text)
    if block_match:
        return block_match.group(1).strip()
    start_match = PYTHON_START_RE.search(text)
    if start_match:
        return text[start_match.start():].strip()
    return text


def _java_filename(code: str) -> str:
    match = PUBLIC_JAVA_TYPE_RE.search(code or "")
    if match:
        return f"{match.group(1)}.java"
    return "RefactoredSample.java"


def _validate_java_code(code: str) -> ValidationStatus:
    status = ValidationStatus(syntax=True, compile=None, structural=None)
    sanitized_code = _sanitize_java_code(code)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            java_path = Path(temp_dir) / _java_filename(sanitized_code)
            java_path.write_text(sanitized_code, encoding="utf-8")
            result = subprocess.run(
                ["javac", str(java_path)],
                capture_output=True,
                text=True,
                check=False,
            )
    except FileNotFoundError:
        status.compile = None
        status.errors.append("javac not available; compile validation skipped")
        return status
    except OSError as exc:
        status.compile = None
        status.errors.append(f"java validation unavailable: {exc}")
        return status

    status.compile = result.returncode == 0
    if result.returncode != 0:
        status.syntax = False
        status.errors.append(result.stderr.strip() or "javac compilation failed")
    return status


def validate_code(code: str, language: str, validation_level: str = "syntax") -> ValidationStatus:
    normalized_language = language.strip().lower()
    if normalized_language == "python":
        is_valid = validate_python(_sanitize_python_code(code))
        status = ValidationStatus(syntax=is_valid, compile=None, structural=None)
        if not is_valid:
            status.errors.append("Python syntax validation failed")
        return status
    if normalized_language == "java":
        return _validate_java_code(code)

    status = ValidationStatus(syntax=False, compile=None, structural=None)
    status.errors.append(f"Unsupported language: {language}")
    return status
