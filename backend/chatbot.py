'''import requests

API = "http://localhost:8000/analyze"


def chat():

    print("Code Smell Detection Chatbot")
    print("----------------------------")

    while True:

        path = input("Enter Java file path (or exit): ")

        if path == "exit":
            break

        files = {"file": open(path, "rb")}

        response = requests.post(API, files=files)

        print("\nDetected Smells:\n")

        print(response.json())


chat()'''

import requests
import json

API = "http://localhost:8000/analyze"

def chat():
    print("========================================")
    print("   Code Smell Analysis Chatbot (CLI)    ")
    print("========================================\n")

    while True:
        path = input("Enter Java file path (or 'exit' to quit): ")

        if path.lower() == "exit":
            break

        if not os.path.exists(path):
            print("File not found. Please try again.")
            continue

        try:
            with open(path, "rb") as f:
                files = {"file": f}
                response = requests.post(API, files=files)

            if response.status_code == 200:
                data = response.json()
                
                if "priority_list" in data:
                    print("\n--- Priority List for Refactoring ---\n")
                    for i, item in enumerate(data["priority_list"], 1):
                        print(f"{i}. [{item['ui_severity']}] {item['smell']}")
                        print(f"   Priority Score: {item['priority_score']}")
                        print(f"   Explanation: {item['explanation']}")
                        print("-" * 40)
                else:
                    print("\nRaw Engine Results:")
                    print(json.dumps(data, indent=2))
            else:
                print(f"Error: Server returned status code {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    import os
    chat()