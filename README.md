# SmellSense AI: Automated Code Smell Detection & Analysis

SmellSense AI is a high-performance system designed to detect, explain, and prioritize code smells in Java applications. It uses a multi-engine approach (Static, Metric, and LLM) to provide comprehensive insights and a prioritized refactoring roadmap.

## Key Features

- **Multi-Engine Detection**: Combines static analysis, code metrics, and LLM-based detection.
- **Parallel Pipeline**: Optimized analysis using parallel processing, reducing wait times by up to 85%.
- **Prioritized Roadmap**: Automatically calculates priority scores based on smell category and severity.
- **Rich AI Explanations**: Provides context-aware, developer-friendly explanations and precise code locations.
- **Persistence**: Automatically saves a prioritized list of smell names to `data/priority_list.json` for downstream refactoring tools.

## Getting Started

### Prerequisites

- Python 3.10+
- Java Runtime Environment (for metric engine)
- Ollama (running locally)

### Running the System

1. **Start the Backend**:

   ```bash
   python -m backend.app.main
   ```

   The API will be available at `http://localhost:8000`.

2. **Start the UI**:
   ```bash
   python -m streamlit run frontend/ui/chatbot_ui.py
   ```
   The dashboard will be available at `http://localhost:8501`.

## Output

The system generates a `data/priority_list.json` file after each analysis, containing a clean, prioritized list of smell names ready for automated refactoring:

````json
[
    "Empty Catch Block",
    "Poor Method Name",
    "Dead Code",
    "Magic Number"
]```
````
