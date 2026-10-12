"""
Build Structured CSV Dataset from Raw PDF Documents.
Handles text extraction, cleaning, duplicate detection, and validation checks.
"""
import os
import glob
import pandas as pd
from pdf_extractor import PDFExtractor
from preprocessor import clean_document_text, is_valid_document_text

def build_dataset(data_dir="data/raw_pdfs", output_csv="data/dataset.csv"):
    extractor = PDFExtractor()
    records = []
    
    categories = ["invoices", "bills", "receipts"]
    category_labels = {
        "invoices": "Invoice",
        "bills": "Bill",
        "receipts": "Receipt"
    }

    print(f"Starting dataset processing from '{data_dir}'...")

    for cat in categories:
        cat_path = os.path.join(data_dir, cat)
        pdf_files = glob.glob(os.path.join(cat_path, "*.pdf"))
        print(f"Found {len(pdf_files)} PDF files in category '{cat}'")

        for file_path in pdf_files:
            file_name = os.path.basename(file_path)
            extraction_res = extractor.extract_from_file(file_path)
            raw_text = extraction_res["text"]
            cleaned_text = clean_document_text(raw_text)
            
            # Check validity
            valid = is_valid_document_text(raw_text)
            
            records.append({
                "file_name": file_name,
                "file_path": file_path,
                "category": category_labels[cat],
                "raw_text": raw_text,
                "cleaned_text": cleaned_text,
                "page_count": extraction_res["page_count"],
                "char_count": extraction_res["char_count"],
                "extraction_method": extraction_res["method"],
                "is_valid": valid
            })

    df = pd.DataFrame(records)
    print(f"\nTotal raw records collected: {len(df)}")

    # Data Quality & Cleaning
    # 1. Filter out empty or invalid text
    initial_count = len(df)
    df = df[df["is_valid"] == True].copy()
    print(f"Filtered out {initial_count - len(df)} invalid/empty documents.")

    # 2. Check for duplicate content
    duplicates = df.duplicated(subset=["cleaned_text"]).sum()
    print(f"Duplicate documents found based on cleaned text: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates(subset=["cleaned_text"], keep="first").copy()

    # 3. Save structured dataset
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Successfully saved structured dataset with {len(df)} records to: {output_csv}")

    # Display dataset breakdown
    print("\nDataset Summary by Category:")
    print(df["category"].value_counts())
    return df

if __name__ == "__main__":
    build_dataset()
