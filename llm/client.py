import re
import subprocess
from typing import Optional

from openai import OpenAI

from config import LLM_PROVIDER, OLLAMA_MODEL, OLLAMA_PATH, OPENAI_API_KEY, OPENAI_MODEL


def _call_ollama(prompt: str, model_override: Optional[str] = None) -> str:
    model_name = model_override or OLLAMA_MODEL
    process = subprocess.Popen(
        [OLLAMA_PATH, "run", model_name],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore",
    )
    output, error = process.communicate(prompt)
    if process.returncode != 0:
        raise RuntimeError(error.strip() or "Ollama call failed")
    return output.strip()


def _call_openai(prompt: str, model_override: Optional[str] = None) -> str:
    model_name = model_override or OPENAI_MODEL
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set")
    if not model_name:
        raise RuntimeError("OPENAI_MODEL is not set")

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model=model_name,
        input=prompt,
    )
    return (response.output_text or "").strip()


def call_llm(prompt: str, model_override: Optional[str] = None) -> str:
    if LLM_PROVIDER == "openai":
        return _call_openai(prompt, model_override=model_override)
    return _call_ollama(prompt, model_override=model_override)




