
import joblib

model = joblib.load("models/document_classifier.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

text = """
Electricity Bill
Energy consumed: 250 kWh
Total Amount Due: INR 1850
Payment due date: 20 October 2026
"""

features = vectorizer.transform([text])
prediction = model.predict(features)

print("Predicted document category:", prediction[0])
