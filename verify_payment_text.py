"""Verify the payment methods text in Service Charter"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from pypdf import PdfReader

pdf_path = r"hospital_docs\KUTTRH-Service-Charter.pdf"
print(f"Reading: {pdf_path}\n")

reader = PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}\n")

# Search for payment-related text
search_terms = ["payment", "Credit Card", "MPESA", "paybill", "shall be made"]

for page_num, page in enumerate(reader.pages):
    text = page.extract_text()
    
    # Check if any search term is in this page
    if any(term.lower() in text.lower() for term in search_terms):
        print(f"=== PAGE {page_num + 1} ===")
        print(text)
        print("\n" + "="*70 + "\n")
