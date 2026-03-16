from app.result_consolidator import consolidate_results
from app.explanation_generator import generate_explanation
from app.severity_predictor import predict_severity
from app.priority_calculator import calculate_priority
from app.constants import get_category_for_smell
import concurrent.futures
import logging

logger = logging.getLogger(__name__)

def analyze_single_smell(candidate, code):
    """
    Worker function to analyze a single code smell.
    """
    smell_name = candidate["smell"]
    category = get_category_for_smell(smell_name)
    supported_by = candidate["supported_by"]
    evidence = candidate["evidence"]
    
    logger.info(f"Analyzing smell: {smell_name}...")
    
    # Task 4: Explanation Generation
    explanation = generate_explanation(
        smell_name, 
        supported_by, 
        evidence, 
        code
    )

    # Task 5: Severity Prediction
    severity_info = predict_severity(smell_name, category, explanation, code)
    severity_label = severity_info["severity"]

    # Task 7-9: Priority Score Calculation
    priority_info = calculate_priority(smell_name, severity_label, category)
    
    return {
        "smell": smell_name,
        "category": category,
        "supported_by": supported_by,
        "explanation": explanation,
        "location": candidate.get("location", "General"),
        "severity": severity_label,
        "severity_score": priority_info["severity_score"],
        "smell_weight": priority_info["smell_weight"],
        "priority_score": priority_info["priority_score"],
        "ui_severity": priority_info["ui_severity"],
        "evidence": evidence
    }

def run_smell_analysis_pipeline(engine_results, code):
    """
    Orchestrates the Explanation, Severity Prediction, and Priority Scoring module.
    Runs analysis in parallel to optimize performance.
    """
    
    # Task 1: Result Consolidation
    consolidation = consolidate_results(engine_results)
    
    if not consolidation["candidate_smells"]:
        return {
            "engine_summary": consolidation["engine_summary"],
            "priority_list": [],
            "message": "No code smells detected by any engine."
        }

    priority_list = []
    
    # Process candidate smells in parallel
    logger.info(f"Starting parallel analysis for {len(consolidation['candidate_smells'])} smells...")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list of futures
        future_to_smell = {
            executor.submit(analyze_single_smell, candidate, code): candidate["smell"] 
            for candidate in consolidation["candidate_smells"]
        }
        
        for future in concurrent.futures.as_completed(future_to_smell):
            smell_name = future_to_smell[future]
            try:
                result = future.result()
                priority_list.append(result)
            except Exception as e:
                logger.error(f"Error analyzing smell '{smell_name}': {e}")

    # Sort priority list by priority_score descending
    priority_list = sorted(priority_list, key=lambda x: x["priority_score"], reverse=True)

    # Final Response Schema
    return {
        "engine_summary": consolidation["engine_summary"],
        "priority_list": priority_list
    }
