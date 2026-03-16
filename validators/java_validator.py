import subprocess

def validate_java(file_path):
    result = subprocess.run(["javac", file_path], capture_output=True)
    return result.returncode == 0
