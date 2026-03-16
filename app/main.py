from fastapi import FastAPI, UploadFile, File
import shutil
import os

from app.detection_engine import detect_all_smells

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SmellSense AI running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    os.makedirs("temp_processing", exist_ok=True)

    file_path = f"temp_processing/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = detect_all_smells(file_path)

    return result