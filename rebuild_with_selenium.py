"""
Rebuild vector store with Selenium-scraped website content
"""
import os
import sys
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, r"c:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant")

from hospital_retriever import HospitalDocumentRetriever
from langchain_community.vectorstores import FAISS

# Initialize retriever
retriever = HospitalDocumentRetriever()

# Delete existing vector store
vector_store_path = r"c:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant\hospital_vector_store"
if os.path.exists(vector_store_path):
    shutil.rmtree(vector_store_path)
    print("[OK] Deleted old vector store")

# Load KUTRRH-specific PDFs only
hospital_docs_dir = r"c:\Users\ckmat\OneDrive\Documents\Masters ICT Policy\Thesis\Thesis Project\AI Assistant\hospital_docs"
kutrrh_pdfs = [
    "KUTTRH-Service-Charter.pdf",
    "Hospital profile_251230_205707.pdf",
    "Kutrrh_ict_policy.pdf",
    "Quality_Policy_Verion_2.0-01.pdf",
    "Frequently Asked Questions FAQs.pdf"
]

pdf_paths = [os.path.join(hospital_docs_dir, pdf) for pdf in kutrrh_pdfs]
pdf_docs = retriever.load_pdf_documents(pdf_paths)
print(f"[OK] Loaded {len(pdf_docs)} PDF documents")

# Load website content with Selenium for JS pages
website_urls = [
    "https://www.kutrrh.go.ke/",
    "https://www.kutrrh.go.ke/about/",
    "https://www.kutrrh.go.ke/services/",
    "https://www.kutrrh.go.ke/contacts/",
    "https://www.kutrrh.go.ke/board-of-directors/",
    "https://www.kutrrh.go.ke/the-executive/",
    "https://www.kutrrh.go.ke/directorates/"
]

print("\nLoading website content (using Selenium for management pages)...")
website_docs = retriever.load_website_content(website_urls)
print(f"[OK] Loaded {len(website_docs)} website pages")

# Combine all documents
all_docs = pdf_docs + website_docs
print(f"\n[OK] Total documents: {len(all_docs)}")

# Chunk documents
chunks = retriever.chunk_documents(all_docs)
print(f"[OK] Created {len(chunks)} chunks")

# Build vector store directly (bypass load-existing logic)
print("\nBuilding new vector store...")
vector_store = FAISS.from_documents(chunks, retriever.embeddings)
vector_store.save_local(vector_store_path)
print(f"[OK] Vector store saved to {vector_store_path}")

# Verify board/executive content
print("\n=== Content Verification ===")
test_queries = ["Zeinab Gura CEO", "Board of Directors members", "Deputy Directors"]
for query in test_queries:
    results = vector_store.similarity_search(query, k=3)
    print(f"\nQuery: '{query}'")
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get('source', 'Unknown')
        preview = doc.page_content[:200].replace('\n', ' ')
        print(f"  {i}. [{source}] {preview}...")

print("\n[SUCCESS] Vector store rebuild complete with Selenium-scraped content")
