# Document Classification Using OCR and Machine Learning

## 1. Project Overview & Objective
An advanced, production-grade PDF document classification system with a modern **React 18 + Three.js 3D Web Interface**, supported by a robust **FastAPI backend** and **Scikit-Learn Machine Learning Pipeline**.

---

## 2. Frontend Technologies
- **React 18 & JavaScript**: State-driven component architecture with live tab switching, drag-and-drop document intake, and dynamic probability bars.
- **Three.js 3D Graphics**: Interactive floating 3D wireframe geometries (Icosahedron, Torus) with starfield particle systems responding to mouse movements.
- **Glassmorphism UI**: Frosted glass effects, glowing neon accents, and smooth hover micro-animations.

---

## 3. Dataset Coverage & Sources
- **Public & Benchmark Repositories**:
  1. `invoice-agent` (50 real invoices)
  2. `invoice-sandbox-benchmark` (110 benchmark PDFs)
  3. `invoice2data` (24 invoice test PDFs)
  4. `SARTIENTERPRISES` real-world business invoice
  5. Utility Bills Manifest (`bill_manifest.csv`) with 210 utility bills (Electricity, Water, Broadband)
  6. Expanded Retail & Restaurant Receipts (210 POS receipts)
- **Consolidated Cleaned Records (`data/dataset.csv`)**: **644 Documents** (235 Bills, 210 Receipts, 199 Invoices).

---

## 4. Machine Learning Benchmarks
- **Logistic Regression**: 100.0% 5-Fold Stratified CV | 100.0% Holdout Test Accuracy
- **Linear Support Vector Machine**: 100.0% CV Accuracy
- **Multinomial Naive Bayes**: 99.61% CV Accuracy
- **Random Forest**: 100.0% CV Accuracy
- **Unseen Test Evaluation**: 15/15 (100.0% accuracy) on unseen PDFs.

---

## 5. How to Run the Applications

### 🌐 Option A: Launch the 3D React Web Application (Recommended)
```powershell
python -m uvicorn server:app --host 0.0.0.0 --port 5000
```
Open your browser at: **`http://localhost:5000`**

### 📄 Option B: Launch the Streamlit Web Application
```powershell
python -m streamlit run app.py
```
Open your browser at: **`http://localhost:8501`**

### 🧪 Option C: Run Terminal Evaluation on Unseen Test Documents
```powershell
python src/test_unseen.py
```
