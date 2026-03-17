import logging
import sys
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/app_server.log")
    ]
)
logger = logging.getLogger(__name__)

try:
    from fastapi import FastAPI, UploadFile, File
    import shutil
    from backend.app.detection_engine import detect_all_smells
    from backend.app.smell_analyzer import run_smell_analysis_pipeline
except Exception as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    logger.info("Root endpoint hit")
    return {"message": "SmellSense AI running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    logger.info(f"Received file for analysis: {file.filename}")
    try:
        os.makedirs("temp_processing", exist_ok=True)
        file_path = f"temp_processing/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("Running detection engines...")
        engine_results = detect_all_smells(file_path)

        logger.info("Running analysis pipeline...")
        with open(file_path) as f:
            code = f.read()
        
        final_result = run_smell_analysis_pipeline(engine_results, code)
        logger.info("Analysis complete")
        
        # Save ONLY smell names to file for the next engine
        import json
        smell_names = [item["smell"] for item in final_result.get("priority_list", [])]
        with open("data/priority_list.json", "w") as f:
            json.dump(smell_names, f, indent=4)
        logger.info("Priority smell names saved to data/priority_list.json")
        
        return final_result
    except Exception as e:
        logger.exception("Error during analysis")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)