# SmellSense AI: Automated Code Smell Detection, Prioritization & Refactoring

SmellSense AI is a research-based system designed to detect, explain, prioritize, and refactor code smells using a combination of static analysis, metrics, and Large Language Models (LLMs).

---

## 🔍 Detection & Analysis Module

* Multi-engine detection (Static + Metrics + LLM)
* Parallel processing pipeline (faster analysis)
* Context-aware AI explanations
* Generates prioritized smell list in:

  ```
  data/priority_list.json
  ```

---

## 🔧 Refactoring Module (LLM-Based)

* Multi-smell processing
* Strategy selection using a smell catalog
* Supports Python and Java validation
* Automatic repair retry for failed outputs
* Outputs structured results in:

  ```
  outputs/latest_results.json
  ```

---

## 🚀 Key Features

* Automated code smell detection and prioritization
* Intelligent refactoring using LLMs
* End-to-end pipeline from detection → refactoring
* Scalable and modular architecture

---

## ⚙️ Getting Started

### Prerequisites

* Python 3.10+
* Java Runtime Environment
* Ollama (running locally)

---

### Run Backend

```bash
python -m backend.app.main
```

API runs at:
http://localhost:8000

---

### Run Frontend

```bash
streamlit run frontend/ui/chatbot_ui.py
```

UI runs at:
http://localhost:8501

---

## 📂 Outputs

### Detection Output

File:

```
data/priority_list.json
```

Example:

```json
[
  "Empty Catch Block",
  "Poor Method Name",
  "Dead Code",
  "Magic Number"
]
```

---

### Refactoring Output

File:

```
outputs/latest_results.json
```

---

## 👨‍💻 Project Goal

To build an intelligent system that not only detects code smells but also automatically suggests and applies refactoring using LLMs, improving code quality and maintainability.
