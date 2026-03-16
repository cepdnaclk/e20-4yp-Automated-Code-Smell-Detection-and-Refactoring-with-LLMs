import requests

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


chat()