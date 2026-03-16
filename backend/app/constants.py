SMELL_TAXONOMY = {
    "Design": [
        "Unutilized Abstraction", "Unnecessary Abstraction", "Broken Hierarchy",
        "Cyclic-Dependent Modularization", "Broken Modularization", "Deficient Encapsulation",
        "Multifaceted Abstraction", "Insufficient Modularization", "Deficient Hierarchy",
        "Imperative Abstraction"
    ],
    "Implementation": [
        "Long Statement", "Magic Number", "Empty Catch Clause", "Complex Conditional",
        "Long Parameter List", "Long Identifier", "Complex Method", "Missing Default",
        "Duplicate Code", "Large Class"
    ],
    "Architecture": [
        "Unstable Dependency", "Hub-Like Dependency", "Cyclic Dependency",
        "God Component", "Unutilized Interface"
    ],
    "Test": [
        "Hard-Coded Test Data", "Indirect Testing", "Excessive Assertion",
        "General Fixture", "Empty or Unknown Test"
    ]
}

CATEGORY_WEIGHTS = {
    "Architecture": 1.2,
    "Design": 1.0,
    "Implementation": 0.8,
    "Test": 0.7
}

SEVERITY_MAPPING = {
    "Minor": 0.3,
    "Major": 0.6,
    "Critical": 0.9
}

def get_category_for_smell(smell_name):
    for category, smells in SMELL_TAXONOMY.items():
        if smell_name in smells:
            return category
    return "Unknown"
