import requests

def detect_llm(code):

    '''prompt = f"""
You are a software engineering expert.

Analyze the following Java code and detect code smells.

Possible smells include design smells, implementation smells, architecture smells, and test smells.

Java Code:
{code}

Return only the detected smells.
"""'''
    prompt = f"""
You are a software engineering expert.
Analyze the following Java code and detect code smells.

Java Code:
{code}

For each smell detected, provide:
1. Smell Name
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
                #"model": "mistral",
                "model": "deepseek-v3.1:671b-cloud",
                "prompt": prompt,
                "stream": False
            }
        )

        result = response.json()

        return result["response"]

    except:

        return "LLM detection unavailable"