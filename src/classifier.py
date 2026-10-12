"""
Inference Backend Classifier for Document Classification.
Exposes a clean API for predicting category from raw text or PDF bytes.
"""
import os
import joblib
import numpy as np
from pdf_extractor import PDFExtractor
from preprocessor import clean_document_text, is_valid_document_text

class DocumentClassifier:
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.extractor = PDFExtractor()
        
        model_path = os.path.join(models_dir, "document_classifier.pkl")
        vect_path = os.path.join(models_dir, "tfidf_vectorizer.pkl")
        meta_path = os.path.join(models_dir, "model_metadata.pkl")

        if not os.path.exists(model_path) or not os.path.exists(vect_path):
            raise FileNotFoundError("Model or vectorizer file not found. Run model_trainer.py first.")

        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vect_path)
        self.metadata = joblib.load(meta_path) if os.path.exists(meta_path) else {}
        self.classes = list(self.model.classes_)

    def predict_from_text(self, text: str):
        """
        Classifies input text string. Returns prediction dict with probabilities.
        """
        if not is_valid_document_text(text):
            return {
                "prediction": "Unknown / Inconclusive",
                "confidence": 0.0,
                "probabilities": {},
                "cleaned_text": "",
                "status": "warning",
                "message": "Extracted text is empty, unreadable, or insufficient for reliable classification."
            }

        cleaned = clean_document_text(text)
        features = self.vectorizer.transform([cleaned])
        
        # Predict probability if supported, otherwise decision function
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(features)[0]
            prob_dict = {cls: float(prob) for cls, prob in zip(self.classes, probs)}
            best_idx = np.argmax(probs)
            pred_class = self.classes[best_idx]
            confidence = float(probs[best_idx])
        else:
            pred_class = self.model.predict(features)[0]
            confidence = 0.95
            prob_dict = {pred_class: confidence}

        # Check for top keywords contributing to this document
        top_keywords = self._get_influential_keywords(features)

        # Inconclusive threshold check
        if confidence < 0.45:
            return {
                "prediction": "Inconclusive",
                "confidence": confidence,
                "probabilities": prob_dict,
                "cleaned_text": cleaned,
                "top_keywords": top_keywords,
                "status": "inconclusive",
                "message": "Document classification confidence is low. Text contains ambiguous or conflicting keywords."
            }

        return {
            "prediction": pred_class,
            "confidence": confidence,
            "probabilities": prob_dict,
            "cleaned_text": cleaned,
            "top_keywords": top_keywords,
            "status": "success",
            "message": f"Successfully classified as {pred_class} with {confidence*100:.1f}% confidence."
        }

    def predict_from_pdf_bytes(self, pdf_bytes: bytes, filename: str = "uploaded.pdf"):
        """
        Extracts text from PDF bytes and runs classification.
        """
        extract_res = self.extractor.extract_from_bytes(pdf_bytes)
        
        if extract_res.get("error"):
            return {
                "filename": filename,
                "prediction": "Error",
                "confidence": 0.0,
                "status": "error",
                "message": extract_res["error"],
                "extraction": extract_res
            }

        pred_res = self.predict_from_text(extract_res["text"])
        pred_res["filename"] = filename
        pred_res["extraction"] = extract_res
        return pred_res

    def _get_influential_keywords(self, feature_vector, top_n=6):
        feature_names = self.vectorizer.get_feature_names_out()
        coo = feature_vector.tocoo()
        sorted_items = sorted(zip(coo.col, coo.data), key=lambda x: x[1], reverse=True)
        keywords = [feature_names[idx] for idx, _ in sorted_items[:top_n]]
        return keywords
