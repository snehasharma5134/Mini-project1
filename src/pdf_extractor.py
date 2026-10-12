"""
PDF Text Extraction Engine with Hybrid Extraction and OCR Fallback.
Handles digital PDFs, scanned documents, and degraded image handling.
"""
import io
import fitz  # PyMuPDF
from PIL import Image

# Check pytesseract availability
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False


class PDFExtractor:
    def __init__(self, tesseract_cmd=None):
        if tesseract_cmd and PYTESSERACT_AVAILABLE:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_from_bytes(self, pdf_bytes, ocr_fallback=True):
        """
        Extract text from raw PDF bytes. Returns dict with extraction results.
        """
        results = {
            "text": "",
            "page_count": 0,
            "method": "native",
            "is_scanned": False,
            "char_count": 0,
            "error": None
        }

        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            results["page_count"] = len(doc)
            extracted_pages = []

            for page_index in range(len(doc)):
                page = doc[page_index]
                text = page.get_text("text").strip()
                if text:
                    extracted_pages.append(text)

            full_text = "\n\n".join(extracted_pages).strip()

            # If text is too sparse or empty, trigger OCR fallback for scanned PDFs
            if len(full_text) < 30 and ocr_fallback:
                results["is_scanned"] = True
                ocr_pages = []
                for page_index in range(len(doc)):
                    page = doc[page_index]
                    pix = page.get_pixmap(dpi=150)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    if PYTESSERACT_AVAILABLE:
                        try:
                            page_ocr = pytesseract.image_to_string(img)
                            if page_ocr.strip():
                                ocr_pages.append(page_ocr.strip())
                        except Exception as ocr_err:
                            results["error"] = f"OCR engine error: {str(ocr_err)}"
                
                if ocr_pages:
                    full_text = "\n\n".join(ocr_pages).strip()
                    results["method"] = "ocr_tesseract"
                else:
                    results["method"] = "native_empty"
            else:
                results["method"] = "native_fitz"

            results["text"] = full_text
            results["char_count"] = len(full_text)
            doc.close()

        except Exception as e:
            results["error"] = f"Failed to parse PDF document: {str(e)}"

        return results

    def extract_from_file(self, file_path, ocr_fallback=True):
        """
        Extract text directly from a file path.
        """
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        res = self.extract_from_bytes(pdf_bytes, ocr_fallback=ocr_fallback)
        res["file_path"] = file_path
        return res


if __name__ == "__main__":
    extractor = PDFExtractor()
    sample = "data/raw_pdfs/invoices/invoice_01.pdf"
    res = extractor.extract_from_file(sample)
    print(f"Extraction method: {res['method']}")
    print(f"Characters extracted: {res['char_count']}")
    print("Preview:\n", res["text"][:200])
