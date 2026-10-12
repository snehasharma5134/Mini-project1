import sys
import glob
from classifier import DocumentClassifier

classifier = DocumentClassifier()
print("Initialized DocumentClassifier successfully.")

test_files = glob.glob("data/test_pdfs/*.pdf")
print(f"Testing on {len(test_files)} unseen evaluation PDFs:\n")

correct = 0
for f in sorted(test_files):
    with open(f, "rb") as pdf_file:
        data = pdf_file.read()
    res = classifier.predict_from_pdf_bytes(data, filename=f)
    print(f"File: {f}")
    print(f"  Method: {res['extraction']['method']} | Extracted chars: {res['extraction']['char_count']}")
    print(f"  Prediction: {res['prediction']} ({res['confidence']*100:.1f}%)")
    print(f"  Top Keywords: {res.get('top_keywords', [])}")
    print(f"  Status: {res['status']}\n")
    if res['prediction'].lower() in f.lower():
        correct += 1

print(f"Unseen Test Evaluation Accuracy: {correct}/{len(test_files)} ({correct/len(test_files)*100:.1f}%)")
