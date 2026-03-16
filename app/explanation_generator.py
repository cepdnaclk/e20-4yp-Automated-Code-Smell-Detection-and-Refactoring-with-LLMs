import requests

def generate_explanation(primary_smell, supported_by, evidence, code):
    """
    Generates a concise explanation for the detected smell.
    Uses LLM to synthesize engine evidence and code context.
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
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-v3.1:671b-cloud",
                "prompt": prompt,
                "stream": False
            }
        )
        result = response.json()
        explanation = result.get("response", "Could not generate explanation.").strip()
        return explanation
    except Exception as e:
        return f"Error generating explanation: {str(e)}"
