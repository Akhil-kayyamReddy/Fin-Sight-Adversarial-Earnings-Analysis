# ==========================================
# api.py
# ==========================================

import os
import shutil

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from main import run_pipeline

# ==========================================
# CREATE APP
# ==========================================
app = FastAPI(
    title="FinSight API",
    description="Adversarial Earnings Analysis System",
    version="1.0.0"
)

# ==========================================
# ENABLE CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ENSURE DATA FOLDER EXISTS
# ==========================================
os.makedirs("data", exist_ok=True)

# ==========================================
# HOME ROUTE
# ==========================================
@app.get("/")
def home():

    return {
        "message": "🚀 FinSight API Running Successfully"
    }

# ==========================================
# ANALYZE PDF
# ==========================================
@app.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    try:

        # -----------------------------
        # SAVE FILE
        # -----------------------------
        file_path = f"data/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # RUN PIPELINE
        # -----------------------------
        result = run_pipeline(file_path)

        # -----------------------------
        # RETURN RESULT
        # -----------------------------
        return {
            "status": "success",
            "file_name": file.filename,
            "analysis": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }