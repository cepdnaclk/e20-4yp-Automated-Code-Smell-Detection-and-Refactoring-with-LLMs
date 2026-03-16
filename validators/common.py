import subprocess
import tempfile
from pathlib import Path

from models.schemas import ValidationStatus
from validators.python_validator import validate_python


def _validate_java_code(code: str) -> ValidationStatus:
    status = ValidationStatus(syntax=True, compile=None, structural=None)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            java_path = Path(temp_dir) / "RefactoredSample.java"
            java_path.write_text(code, encoding="utf-8")
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
        is_valid = validate_python(code)
        status = ValidationStatus(syntax=is_valid, compile=None, structural=None)
        if not is_valid:
            status.errors.append("Python syntax validation failed")
        return status
    if normalized_language == "java":
        return _validate_java_code(code)

    status = ValidationStatus(syntax=False, compile=None, structural=None)
    status.errors.append(f"Unsupported language: {language}")
    return status
