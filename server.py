"""
FastAPI Backend Server for Modern React + 3D Three.js Frontend.
Exposes endpoints for file upload classification, sample testing, and dataset statistics.
"""
import sys
import os
import glob
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from classifier import DocumentClassifier

app = FastAPI(title="DocuClassify 3D API", description="AI Document Classification with 3D UI", version="2.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Classifier
classifier = DocumentClassifier(models_dir="models")

@app.get("/api/health")
def health():
    return {"status": "ok", "model": classifier.metadata.get("best_model_name", "Logistic Regression")}

@app.post("/api/classify")
async def classify_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    contents = await file.read()
    result = classifier.predict_from_pdf_bytes(contents, filename=file.filename)
    return result

@app.get("/api/samples")
def list_samples():
    sample_files = glob.glob("data/test_pdfs/*.pdf")
    items = []
    for f in sorted(sample_files):
        fname = os.path.basename(f)
        category_hint = "Invoice" if "invoice" in fname.lower() else ("Bill" if "bill" in fname.lower() else "Receipt")
        items.append({
            "filename": fname,
            "path": f,
            "category_hint": category_hint
        })
    return {"samples": items}

@app.get("/api/classify-sample/{filename}")
def classify_sample(filename: str):
    file_path = os.path.join("data/test_pdfs", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Sample PDF not found.")
    
    with open(file_path, "rb") as f:
        content = f.read()
    result = classifier.predict_from_pdf_bytes(content, filename=filename)
    return result

@app.get("/api/analytics")
def get_analytics():
    dataset_path = "data/dataset.csv"
    stats = {
        "total_documents": 0,
        "class_distribution": {},
        "model_benchmarks": classifier.metadata.get("comparison_results", []),
        "confusion_matrix": classifier.metadata.get("confusion_matrix", []),
        "classes": classifier.metadata.get("classes", [])
    }
    
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        stats["total_documents"] = len(df)
        stats["class_distribution"] = df["category"].value_counts().to_dict()
        
    return stats

# Serve Frontend static build / HTML
app.mount("/static", StaticFiles(directory="frontend/public"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("frontend/public/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True)
