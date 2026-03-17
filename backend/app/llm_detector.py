import logging
import os

import requests


logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
DETECTION_MODEL = os.getenv("DETECTION_LLM_MODEL", os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("DETECTION_LLM_TIMEOUT_SECONDS", "20"))
MAX_CODE_CHARS = int(os.getenv("DETECTION_LLM_MAX_CODE_CHARS", "3000"))


def _trim_code(code: str) -> str:
    trimmed = (code or "").strip()
    if len(trimmed) <= MAX_CODE_CHARS:
        return trimmed
    return trimmed[:MAX_CODE_CHARS] + "\n// [truncated for faster smell detection]"


def detect_llm(code):
    prompt = (
        "Detect up to 3 code smells in this Java code.\n\n"
        "Return only one line per smell in this format:\n"
        "SMELL: <name> | LOCATION: <method/class/line> | DESCRIPTION: <short reason>\n\n"
        "Code:\n"
        f"{_trim_code(code)}"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": DETECTION_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip() or "LLM detection unavailable"
    except Exception as exc:
        logger.warning("LLM detection failed using model '%s': %s", DETECTION_MODEL, exc)
        return "LLM detection unavailable"
