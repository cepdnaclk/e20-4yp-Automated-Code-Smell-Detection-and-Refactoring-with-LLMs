import re

def detect_static(code):

    smells = []

    # Magic Number
    if re.search(r'\b\d+\b', code):
        smells.append("Magic Number")

    # Empty Catch Clause
    if "catch(Exception e){}" in code.replace(" ", ""):
        smells.append("Empty Catch Clause")

    # Missing Default
    if "switch" in code and "default" not in code:
        smells.append("Missing Default")

    # Complex Conditional
    if code.count("if(") > 3:
        smells.append("Complex Conditional")

    # Long Statement
    if len(code.split("\n")) > 300:
        smells.append("Long Statement")

    return smells