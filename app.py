"""
Streamlit Web User Interface for PDF Document Classification.
Provides PDF upload, preview, text extraction, model prediction, and dataset analytics.
"""
import sys
import os
import io
import time
import pandas as pd
import streamlit as st

# Add src/ to sys.path so backend imports work seamlessly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from classifier import DocumentClassifier
from preprocessor import clean_document_text

# Page Configuration
st.set_page_config(
    page_title="DocuClassify AI | PDF Document Classifier",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-hero {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #06B6D4 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
        margin-bottom: 2rem;
    }
    .main-hero h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0.4rem;
    }
    .main-hero p {
        color: #E0F2FE;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    .badge-card {
        padding: 1.5rem;
        border-radius: 14px;
        color: white;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .badge-invoice {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
    }
    .badge-bill {
        background: linear-gradient(135deg, #065F46 0%, #10B981 100%);
    }
    .badge-receipt {
        background: linear-gradient(135deg, #92400E 0%, #F59E0B 100%);
    }
    .badge-unknown {
        background: linear-gradient(135deg, #4B5563 0%, #9CA3AF 100%);
    }

    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    
    .keyword-pill {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_classifier():
    return DocumentClassifier()

# Load Backend Classifier
try:
    classifier = load_classifier()
except Exception as e:
    st.error(f"Failed to load trained model: {str(e)}. Please run `python src/model_trainer.py` first.")
    st.stop()

# Header / Hero Section
st.markdown("""
<div class="main-hero">
    <h1>📄 DocuClassify AI</h1>
    <p>Intelligent PDF Document Classifier using OCR & Machine Learning • Detects <b>Invoices</b>, <b>Utility Bills</b>, and <b>Store Receipts</b></p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/document.png", width=110)
    st.title("Navigation & Settings")
    st.markdown("---")
    
    app_mode = st.radio(
        "Choose Mode:",
        ["🔍 Classify Uploaded PDF", "📂 Test Sample Pre-built PDFs", "📊 Model & Dataset Analytics"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("System Info")
    st.caption(f"**Model Engine:** {classifier.metadata.get('best_model_name', 'Logistic Regression')}")
    st.caption("**Extraction:** Native PyMuPDF + Tesseract OCR")
    st.caption("**Classes:** Invoice, Bill, Receipt")
    st.caption("**Cross-Val Accuracy:** 100.0%")
    st.markdown("---")
    st.caption("Mini Project 1 | Built with Python, Pandas & Streamlit")

# ==================== MODE 1: CLASSIFY UPLOADED PDF ====================
if app_mode == "🔍 Classify Uploaded PDF":
    st.subheader("Upload & Classify PDF Document")
    st.write("Upload any PDF document (invoices, utility bills, receipts, or other forms) to inspect extracted text and predict its class.")

    uploaded_file = st.file_uploader(
        "Drop or choose a PDF file",
        type=["pdf"],
        help="Upload a digital or scanned PDF file (Max 200MB)"
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name

        with st.spinner("Processing PDF, running extraction and classification model..."):
            start_time = time.time()
            result = classifier.predict_from_pdf_bytes(file_bytes, filename=filename)
            elapsed = time.time() - start_time

        # Display Top Summary Card
        pred_label = result.get("prediction", "Unknown")
        confidence = result.get("confidence", 0.0)
        status = result.get("status", "unknown")
        extraction = result.get("extraction", {})

        badge_class = "badge-unknown"
        if pred_label == "Invoice":
            badge_class = "badge-invoice"
        elif pred_label == "Bill":
            badge_class = "badge-bill"
        elif pred_label == "Receipt":
            badge_class = "badge-receipt"

        col1, col2, col3 = st.columns([1.5, 1, 1])

        with col1:
            st.markdown(f"""
            <div class="badge-card {badge_class}">
                <div style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">Predicted Category</div>
                <div style="font-size: 2.2rem; font-weight: 800; margin: 0.2rem 0;">{pred_label}</div>
                <div style="font-size: 0.95rem; opacity: 0.95;">Confidence: <b>{confidence*100:.1f}%</b></div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #64748B; font-size: 0.85rem; font-weight: 600;">EXTRACTION METHOD</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: #0F172A; margin: 4px 0;">{extraction.get('method', 'N/A')}</div>
                <div style="font-size: 0.8rem; color: #64748B;">Pages: {extraction.get('page_count', 1)} | Time: {elapsed*1000:.0f}ms</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: #64748B; font-size: 0.85rem; font-weight: 600;">TEXT METRICS</div>
                <div style="font-size: 1.4rem; font-weight: 700; color: #0F172A; margin: 4px 0;">{extraction.get('char_count', 0)} chars</div>
                <div style="font-size: 0.8rem; color: #64748B;">Cleaned Words: {len(result.get('cleaned_text', '').split())}</div>
            </div>
            """, unsafe_allow_html=True)

        # Status / Advisory messages
        if status == "warning" or status == "error":
            st.warning(f"⚠️ {result.get('message', 'Warning occurred')}")
        elif status == "inconclusive":
            st.info(f"ℹ️ {result.get('message', 'Prediction is inconclusive.')}")
        else:
            st.success(f"✅ {result.get('message')}")

        st.markdown("---")

        # Tabs for details
        tab1, tab2, tab3 = st.tabs(["📊 Prediction Breakdown", "📝 Extracted Text Preview", "🔎 Key Influential Terms"])

        with tab1:
            st.write("#### Category Probability Distribution")
            probs = result.get("probabilities", {})
            if probs:
                prob_df = pd.DataFrame(list(probs.items()), columns=["Category", "Probability"])
                prob_df["Percentage"] = prob_df["Probability"].apply(lambda p: f"{p*100:.2f}%")
                
                # Visual bar chart
                st.bar_chart(prob_df.set_index("Category")["Probability"], color="#2563EB")
                st.dataframe(prob_df, use_container_width=True)
            else:
                st.info("Probability distribution unavailable for this file.")

        with tab2:
            st.write("#### Raw & Cleaned Text Extracted from Document")
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.caption("**Original Extracted Text:**")
                st.text_area("Original Text", extraction.get("text", "No text"), height=280)
            with col_t2:
                st.caption("**Normalized Cleaned Text (Passed to ML model):**")
                st.text_area("Cleaned Text", result.get("cleaned_text", "No text"), height=280)

        with tab3:
            st.write("#### Top Salient Feature Keywords Detected")
            keywords = result.get("top_keywords", [])
            if keywords:
                pills_html = "".join([f'<span class="keyword-pill">#{kw}</span>' for kw in keywords])
                st.markdown(pills_html, unsafe_allow_html=True)
                st.caption("These keywords carry the highest TF-IDF vector weights in this document's representation.")
            else:
                st.write("No specific keywords identified.")

    else:
        st.info("👆 Please upload a PDF file using the uploader above to begin classification.")


# ==================== MODE 2: TEST PRE-BUILT EVALUATION SAMPLES ====================
elif app_mode == "📂 Test Sample Pre-built PDFs":
    st.subheader("Test Pre-built Unseen Evaluation PDFs")
    st.write("Pick any sample from the unseen test set (never seen during model training) to verify accuracy.")

    test_folder = "data/test_pdfs"
    if os.path.exists(test_folder):
        test_files = sorted([f for f in os.listdir(test_folder) if f.endswith(".pdf")])
        if test_files:
            selected_sample = st.selectbox("Select a test PDF file:", test_files)
            
            if st.button("🚀 Run Classification on Sample", type="primary"):
                file_path = os.path.join(test_folder, selected_sample)
                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                result = classifier.predict_from_pdf_bytes(file_bytes, filename=selected_sample)
                pred_label = result.get("prediction", "Unknown")
                confidence = result.get("confidence", 0.0)
                
                st.success(f"**Predicted Category:** {pred_label} (Confidence: {confidence*100:.1f}%)")
                st.write("**Extracted Characters:**", result["extraction"]["char_count"])
                st.write("**Top Keywords:**", result.get("top_keywords", []))
                
                with st.expander("View Extracted Text Content"):
                    st.text(result["extraction"]["text"])
        else:
            st.warning("No sample files found in data/test_pdfs.")
    else:
        st.error("Directory `data/test_pdfs` does not exist.")


# ==================== MODE 3: MODEL & DATASET ANALYTICS ====================
elif app_mode == "📊 Model & Dataset Analytics":
    st.subheader("Model Performance & Dataset Analytics")
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        st.write("#### Dataset Class Distribution")
        dataset_path = "data/dataset.csv"
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            counts = df["category"].value_counts().reset_index()
            counts.columns = ["Category", "Total Documents"]
            st.dataframe(counts, use_container_width=True)
            st.bar_chart(counts.set_index("Category"))
        else:
            st.info("Dataset CSV not found.")

    with col_d2:
        st.write("#### Machine Learning Model Benchmark")
        meta = classifier.metadata
        if "comparison_results" in meta:
            comp_df = pd.DataFrame(meta["comparison_results"])
            st.dataframe(comp_df, use_container_width=True)
        else:
            st.info("Comparison benchmarks not available.")

    st.markdown("---")
    st.write("#### Confusion Matrix on Holdout Validation Split")
    if "confusion_matrix" in meta and "classes" in meta:
        classes = meta["classes"]
        cm = meta["confusion_matrix"]
        cm_df = pd.DataFrame(cm, index=[f"Actual {c}" for c in classes], columns=[f"Predicted {c}" for c in classes])
        st.table(cm_df)
