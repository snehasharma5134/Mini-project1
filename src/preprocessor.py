"""
Text Preprocessing and Cleaning Module for Document Classification.
Handles cleaning, punctuation/whitespace normalization, and feature tokenization.
"""
import re
import string

def clean_document_text(text: str) -> str:
    """
    Cleans extracted document text for machine learning.
    1. Lowers case
    2. Normalizes line breaks and whitespace
    3. Retains informative punctuation / removes noise
    """
    if not text or not isinstance(text, str):
        return ""

    # Replace newlines and tabs with spaces
    cleaned = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")

    # Lowercase
    cleaned = cleaned.lower()

    # Normalize special monetary and numeric signs
    cleaned = re.sub(r'[\$€£₹]', ' currency ', cleaned)
    
    # Remove excessive punctuation while keeping alphanumeric tokens and key markers
    cleaned = re.sub(r'[^\w\s]', ' ', cleaned)

    # Collapse multiple spaces into single space
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def is_valid_document_text(text: str, min_chars: int = 25) -> bool:
    """
    Validates whether the extracted text contains meaningful content.
    Filters out empty, corrupted, or blank scans.
    """
    if not text or not isinstance(text, str):
        return False
    cleaned = clean_document_text(text)
    return len(cleaned) >= min_chars
