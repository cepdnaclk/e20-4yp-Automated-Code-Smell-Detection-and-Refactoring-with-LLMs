import logging
import os
import requests
from backend.app.constants import SMELL_TAXONOMY

logger = logging.getLogger(__name__)

# Configurations (your part)
OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
DETECTION_MODEL = os.getenv(
    "DETECTION_LLM_MODEL",
    os.getenv("OLLAMA_MODEL", "deepseek-v3.1:671b-cloud")
)
REQUEST_TIMEOUT_SECONDS = int(os.getenv("DETECTION_LLM_TIMEOUT_SECONDS", "20"))
MAX_CODE_CHARS = int(os.getenv("DETECTION_LLM_MAX_CODE_CHARS", "3000"))


def _trim_code(code: str) -> str:
    trimmed = (code or "").strip()
    if len(trimmed) <= MAX_CODE_CHARS:
        return trimmed
    return trimmed[:MAX_CODE_CHARS] + "\n// [truncated for faster smell detection]"


def detect_llm(code: str):
    # Flatten taxonomy (friend's logic)
    all_allowed_smells = []
    for category, smells in SMELL_TAXONOMY.items():
        all_allowed_smells.extend(smells)

    allowed_smells_str = ", ".join(all_allowed_smells)

    # Combined prompt (clean + structured)
    prompt = f"""
You are a software engineering expert.

Analyze the following Java code and detect up to 3 code smells.

IMPORTANT:
- ONLY use these smell names:
{allowed_smells_str}

For each detected smell, return ONE line in this format:
SMELL: <name> | LOCATION: <method/class/line> | DESCRIPTION: <short reason>

Java Code:
{_trim_code(code)}
"""

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
        logger.warning(
            "LLM detection failed using model '%s': %s",
            DETECTION_MODEL,
            exc
        )
        return "LLM detection unavailable"