import requests

def detect_llm(code):

    prompt = f"""
You are a software engineering expert.

Analyze the following Java code and detect code smells.

Possible smells include design smells, implementation smells, architecture smells, and test smells.

Java Code:
{code}

Return only the detected smells.
"""

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        return result["response"]

    except:

        return "LLM detection unavailable"