import logging
import os

import requests


logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
EXPLANATION_MODEL = os.getenv(
    "EXPLANATION_LLM_MODEL",
    os.getenv("DETECTION_LLM_MODEL", os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b")),
)
REQUEST_TIMEOUT_SECONDS = int(os.getenv("EXPLANATION_LLM_TIMEOUT_SECONDS", "20"))


def _fallback_explanation(primary_smell, supported_by, evidence):
    engines_str = ", ".join(supported_by) if supported_by else "one detection engine"
    first_evidence = evidence[0] if evidence else f"The code matches known patterns for {primary_smell}."
    return (
        f"{primary_smell} was flagged by {engines_str}. "
        f"{first_evidence} This can reduce readability and maintainability if left unresolved."
    )


def generate_explanation(primary_smell, supported_by, evidence, code):
    """
    Generates a concise explanation for the detected smell.
    Uses LLM to synthesize engine evidence and code context, with a deterministic fallback.
    """

    engines_str = ", ".join(supported_by)
    evidence_str = "\n- ".join(evidence)

    prompt = f"""
You are a software quality expert.
Analyze the following code smell and the evidence provided by multiple detection engines.

Primary Smell: {primary_smell}
Detected by: {engines_str}
Evidence from engines:
- {evidence_str}

Code Snippet:
{code}

Task:
Generate a concise, developer-friendly explanation for this code smell.
Rules:
- Mention concrete code issues found in the snippet.
- Do not use generic explanations.
- Keep it short (1-2 sentences).
- Reflect the strength of support (multiple engines) if applicable.
- Focus on why this is a problem for readability or maintainability.

Explanation:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": EXPLANATION_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        explanation = result.get("response", "").strip()
        return explanation or _fallback_explanation(primary_smell, supported_by, evidence)
    except Exception as exc:
        logger.warning("Explanation generation failed using model '%s': %s", EXPLANATION_MODEL, exc)
        return _fallback_explanation(primary_smell, supported_by, evidence)
