import requests
import json

def predict_severity(primary_smell, category, explanation, code):
    """
    Predicts the severity of the primary smell using LLM.
    Returns a dictionary with 'severity' and 'reason'.
    """
    
    prompt = f"""
You are a software quality expert.
Analyze the following code smell and its explanation to determine its severity.

Primary Smell: {primary_smell}
Category: {category}
Explanation: {explanation}

Context Definitions:
- Minor: Small maintainability issue with limited impact.
- Major: Significant maintainability or readability issue.
- Critical: Severe design or architectural issue with high impact.

Code Snippet:
{code}

Task:
1. Classify the severity of this smell into EXACTLY one of: Minor, Major, Critical.
2. Provide a brief reason for this classification.

Return the result as a raw JSON object with keys "severity" and "reason".
Example:
{{"severity": "Major", "reason": "The smell significantly affects maintainability but is not a structural failure."}}

Result:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-v3.1:671b-cloud",
                "prompt": prompt,
                "stream": False,
                "format": "json"
            }
        )
        result = response.json()
        severity_data = json.loads(result.get("response", "{}"))
        
        # Validate severity label
        severity = severity_data.get("severity", "Major")
        if severity not in ["Minor", "Major", "Critical"]:
            severity = "Major" # Default to Major if invalid
            
        reason = severity_data.get("reason", "Severity predicted based on smell category and code context.")
        
        return {
            "severity": severity,
            "reason": reason
        }
    except Exception as e:
        return {
            "severity": "Major",
            "reason": f"External predictor error: {str(e)}"
        }
