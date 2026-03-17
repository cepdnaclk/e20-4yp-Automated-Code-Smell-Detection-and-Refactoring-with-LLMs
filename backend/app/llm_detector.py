from backend.app.constants import SMELL_TAXONOMY
import requests

def detect_llm(code):
    # Flatten the taxonomy for the prompt
    all_allowed_smells = []
    for category, smells in SMELL_TAXONOMY.items():
        all_allowed_smells.extend(smells)
    
    allowed_smells_str = ", ".join(all_allowed_smells)

    prompt = f"""
You are a software engineering expert.
Analyze the following Java code and detect code smells.

IMPORTANT: You must ONLY use the following established code smell names:
{allowed_smells_str}

Java Code:
{code}

For each smell detected, provide:
1. Smell Name (Must be from the list above)
2. Location (Line number or Method name)
3. Brief Technical Explanation (why it's a problem)

Format your response AS A LIST where each item is:
SMELL: [Name] | LOCATION: [Location] | DESCRIPTION: [Description]

Return ONLY the list.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-v3.1:671b-cloud",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        return result["response"]

    except:

        return "LLM detection unavailable"