from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

INPUT_ANALYSIS_PATH = Path(
    os.getenv("ANALYSIS_FILE", str(BASE_DIR / "detection_results" / "analysis.json"))
)
DETECTION_HANDOFF_PATH = BASE_DIR / "detection_results" / "from_detection.json"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
EXPERIMENTS_DIR = OUTPUTS_DIR / "experiments"
PROMPTS_DIR = BASE_DIR / "prompts"
RULES_DIR = BASE_DIR / "rules"

DEFAULT_OUTPUT_PATH = OUTPUTS_DIR / "latest_results.json"
SMELL_CATALOG_PATH = RULES_DIR / "smell_catalog.json"

# Force Ollama for now
LLM_PROVIDER = "ollama"

# Hardcode executable path to avoid environment variable conflicts
OLLAMA_PATH = r"C:\Users\Dharani\AppData\Local\Programs\Ollama\ollama.exe"

# Use a model that is actually installed
OLLAMA_MODEL = "deepseek-v3.1:671b-cloud"
OLLAMA_MODELS = [OLLAMA_MODEL]

# Keep OpenAI config present but inactive
OPENAI_API_KEY = ""
OPENAI_MODEL = ""