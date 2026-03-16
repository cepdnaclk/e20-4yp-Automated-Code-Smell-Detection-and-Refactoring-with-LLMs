import uvicorn
import os
import sys

# Ensure current directory is in sys.path
sys.path.append(os.getcwd())

if __name__ == "__main__":
    from app.main import app
    print("Starting server on port 8005...")
    uvicorn.run(app, host="0.0.0.0", port=8005)