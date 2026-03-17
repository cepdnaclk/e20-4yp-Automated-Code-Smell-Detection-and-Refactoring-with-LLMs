from backend.app.constants import get_category_for_smell
import re

def consolidate_results(engine_results):
    """
    Consolidates results from static_engine, metric_engine, and llm_engine.
    Input format for llm_engine is now structured:
    SMELL: [Name] | LOCATION: [Location] | DESCRIPTION: [Description]
    """
    
    # Normalize inputs
    normalized_results = {}
    llm_raw_lines = []
    
    # Static Engine
    static_smells = engine_results.get("static_engine", [])
    if isinstance(static_smells, str):
        static_smells = [s.strip() for s in static_smells.split(",") if s.strip()]
    normalized_results["static_engine"] = static_smells
    
    # Metric Engine
    metric_smells = engine_results.get("metric_engine", [])
    if isinstance(metric_smells, str):
        metric_smells = [s.strip() for s in metric_smells.split(",") if s.strip()]
    normalized_results["metric_engine"] = metric_smells
    
    # LLM Engine - Handle structured output
    llm_output = engine_results.get("llm_engine", "")
    llm_entities = []
    if isinstance(llm_output, str):
        # Pattern to match: SMELL: [Name] | LOCATION: [Location] | DESCRIPTION: [Description]
        # We use a non-greedy match to handle multiple items in one line or split by lines
        pattern = r"SMELL:\s*(.*?)\s*(?:\||LOCATION:)\s*(.*?)\s*(?:\||DESCRIPTION:)\s*(.*?)(?=$|SMELL:)"
        matches = re.finditer(pattern, llm_output, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            name = match.group(1).strip().strip("[]")
            location = match.group(2).strip().strip("[]")
            description = match.group(3).strip().strip("[]")
            
            if name:
                llm_entities.append({
                    "name": name,
                    "location": location,
                    "description": description
                })
                llm_raw_lines.append(name)
    
    normalized_results["llm_engine"] = llm_raw_lines
    
    # Group smells and collect support/evidence
    candidate_map = {}
    
    # Handle Static and Metric first
    for engine in ["static_engine", "metric_engine"]:
        for smell in normalized_results[engine]:
            if get_category_for_smell(smell) == "Unknown":
                continue

            if smell not in candidate_map:
                candidate_map[smell] = {
                    "smell": smell,
                    "supported_by": [],
                    "evidence": [],
                    "location": "General"
                }
            if engine not in candidate_map[smell]["supported_by"]:
                candidate_map[smell]["supported_by"].append(engine)
                
            if engine == "static_engine":
                candidate_map[smell]["evidence"].append(f"Static analysis detected {smell} patterns.")
            elif engine == "metric_engine":
                candidate_map[smell]["evidence"].append(f"Metric analysis exceeded threshold for {smell}.")

    # Handle LLM with structured data
    for entity in llm_entities:
        name = entity["name"]
        location = entity["location"]
        description = entity["description"]
        
        if get_category_for_smell(name) == "Unknown":
            continue

        # Simple fuzzy matching for duplicates (if LLM name slightly differs from Static/Metric)
        # For now, let's keep it exact or add to existing if it matches
        matched = False
        for existing_smell in candidate_map:
            if name.lower() in existing_smell.lower() or existing_smell.lower() in name.lower():
                candidate_map[existing_smell]["supported_by"].append("llm_engine")
                candidate_map[existing_smell]["evidence"].append(f"LLM confirmed: {description}")
                if location and candidate_map[existing_smell]["location"] == "General":
                    candidate_map[existing_smell]["location"] = location
                matched = True
                break
        
        if not matched:
            candidate_map[name] = {
                "smell": name,
                "supported_by": ["llm_engine"],
                "evidence": [f"LLM identified: {description}"],
                "location": location if location else "General"
            }

    candidate_smells = list(candidate_map.values())
    
    # Determine primary smell (largest support)
    primary_smell = None
    if candidate_smells:
        sorted_candidates = sorted(candidate_smells, key=lambda x: (-len(x["supported_by"]), x["smell"]))
        primary_smell = sorted_candidates[0]["smell"]
    
    category = get_category_for_smell(primary_smell) if primary_smell else "Unknown"
    
    return {
        "engine_summary": normalized_results,
        "candidate_smells": candidate_smells,
        "primary_smell": primary_smell,
        "category": category
    }
