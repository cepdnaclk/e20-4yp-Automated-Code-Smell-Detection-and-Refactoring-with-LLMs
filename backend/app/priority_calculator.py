from backend.app.constants import SEVERITY_MAPPING, CATEGORY_WEIGHTS

def calculate_priority(primary_smell, severity_label, category):
    """
    Calculates the priority score and UI severity.
    """
    
    severity_score = SEVERITY_MAPPING.get(severity_label, 0.6) # Default to Major score
    smell_weight = CATEGORY_WEIGHTS.get(category, 1.0) # Default weight
    
    priority_score = round(severity_score * smell_weight, 2)
    ui_severity = f"{round(priority_score * 5, 1)}/5"
    
    return {
        "severity_score": severity_score,
        "smell_weight": smell_weight,
        "priority_score": priority_score,
        "ui_severity": ui_severity
    }
