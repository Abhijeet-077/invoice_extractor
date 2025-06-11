import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import re
from PIL import Image

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    # If not enough text, fallback to OCR
    if len(text.strip()) < 100:
        print("[INFO] Falling back to OCR...")
        text = extract_text_with_ocr(file_path)
    return text

def extract_text_with_ocr(file_path):
    images = convert_from_path(file_path)
    full_text = ""
    for image in images:
        bw = image.convert("L")  # Convert to grayscale
        ocr_text = pytesseract.image_to_string(bw)
        full_text += ocr_text + "\n"
    return full_text

def extract_invoice_data(file_path):
    text = extract_text_from_pdf(file_path)

    print("========== FULL EXTRACTED TEXT ==========")
    print(text[:1000])  # Optional: Preview first 1000 chars
    print("=========================================")

    # Extract metadata
    invoice_number = re.search(r"Invoice\s*Number\s*[:\-]?\s*([A-Z0-9\-]+)", text, re.IGNORECASE)
    invoice_date = re.search(r"(Invoice\s+Date\s*[:\-]?\s*)(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})", text, re.IGNORECASE)
    vendor = re.search(r"Sold By\s*:?\s*(.*?)\s*(Billing Address|PAN No|GST)", text, re.IGNORECASE | re.DOTALL)
    buyer = re.search(
        r"(Bill(?:ed)?\s*To|Sold\s*To|Billing Address|Ship(?:ping)?\s*To)\s*[:\-]?\s*(.*?)\s*(Shipping Address|GSTIN|State|\n{2,})",
        text, re.IGNORECASE | re.DOTALL
    )
    payment_mode = re.search(
        r"(?:Payment\s*(Mode|Method)|Mode\s*of\s*Payment|paid\s*via|payment\s+is\s+of)\s*[:\-]?\s*([A-Za-z0-9 ]+)",
        text, re.IGNORECASE
    )
    total_amount = re.search(r"(?:TOTAL|Grand\s*Total)\s*[:\-]?\s*[₹$]?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)
    tax_amount = re.search(r"(?:Tax|GST)\s*[:\-]?\s*[₹$]?\s*([\d,]+\.\d{2})", text, re.IGNORECASE)

    meta_data = {
        "Invoice Number": invoice_number.group(1) if invoice_number else None,
        "Invoice Date": invoice_date.group(2) if invoice_date else None,
        "Vendor": vendor.group(1).replace('\n', ' ').strip() if vendor else None,
        "Buyer": buyer.group(2).replace('\n', ' ').strip() if buyer else None,
        "Total Amount": total_amount.group(1).replace(',', '') if total_amount else None,
        "Tax Amount": tax_amount.group(1).replace(',', '') if tax_amount else None,
        "Payment Mode": payment_mode.group(2).strip() if payment_mode else None
    }

    return meta_data
