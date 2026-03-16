from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent
INPUT_ANALYSIS_PATH = Path(os.getenv("ANALYSIS_FILE", str(BASE_DIR / "detection_results" / "analysis.json")))
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "outputs"
EXPERIMENTS_DIR = OUTPUTS_DIR / "experiments"
PROMPTS_DIR = BASE_DIR / "prompts"
RULES_DIR = BASE_DIR / "rules"

DEFAULT_OUTPUT_PATH = OUTPUTS_DIR / "latest_results.json"
SMELL_CATALOG_PATH = RULES_DIR / "smell_catalog.json"

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").strip().lower()

OLLAMA_PATH = os.getenv(
    "OLLAMA_PATH",
    r"C:\Users\Dhananji\AppData\Local\Programs\Ollama\ollama.exe",
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder:6.7b")
OLLAMA_MODELS = [model.strip() for model in os.getenv("OLLAMA_MODELS", OLLAMA_MODEL).split(",") if model.strip()]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")
