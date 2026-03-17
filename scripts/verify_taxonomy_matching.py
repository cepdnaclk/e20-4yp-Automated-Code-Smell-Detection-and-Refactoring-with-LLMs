import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from backend.app.result_consolidator import consolidate_results
import json

def test_normalization():
    print("Testing taxonomy normalization...")
    
    # Mock engine results with names that should be normalized
    engine_results = {
        "static_engine": [],
        "metric_engine": [],
        "llm_engine": "SMELL: God Object | LOCATION: UniversityManager class | DESCRIPTION: The class has too many responsibilities.\nSMELL: SRP Violation | LOCATION: StudentService | DESCRIPTION: Violates single responsibility principle."
    }
    
    result = consolidate_results(engine_results)
    candidate_smells = result["candidate_smells"]
    
    smell_names = [c["smell"] for c in candidate_smells]
    print(f"Detected smells: {smell_names}")
    
    # Check if 'God Object' was mapped to 'God Component'
    # And if 'SRP Violation' was mapped to 'Large Class'
    expected_mappings = {
        "God Component": "God Object",
        "Large Class": "SRP Violation"
    }
    
    all_passed = True
    for official, raw in expected_mappings.items():
        if official in smell_names:
            print(f"✅ PASSED: Successfully mapped '{raw}' to '{official}'")
        else:
            print(f"❌ FAILED: Could not find '{official}' in results (was looking for mapping from '{raw}')")
            all_passed = False
            
    if all_passed:
        print("\nAll normalization tests passed!")
    else:
        print("\nSome normalization tests failed.")
        sys.exit(1)

if __name__ == "__main__":
    test_normalization()
