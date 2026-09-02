#!/usr/bin/env python3
"""
Initialize Hospital Knowledge Base
Run this script to build the vector store from hospital documents and website
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from hospital_setup import setup_hospital_knowledge_base
from logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Initialize the hospital knowledge base"""
    
    print("\n" + "="*60)
    print("🏥 Hospital Knowledge Base Initialization")
    print("="*60 + "\n")
    
    print("📁 Checking for hospital documents...")
    
    # Check if hospital_docs folder exists
    if not os.path.exists("hospital_docs"):
        print("⚠️  No 'hospital_docs' folder found.")
        print("   Please create 'hospital_docs' folder and add hospital PDF files.")
        print("   Example: mkdir hospital_docs")
        return False
    
    # Count PDF files
    pdf_files = [f for f in os.listdir("hospital_docs") if f.lower().endswith('.pdf')]
    
    if pdf_files:
        print(f"\n✅ Found {len(pdf_files)} hospital document(s):")
        for pdf_file in pdf_files:
            print(f"   • {pdf_file}")
    else:
        print("\n⚠️  No PDF files found in 'hospital_docs' folder.")
        print("   The system will attempt to scrape the hospital website.")
    
    print("\n🌐 Website URLs to be used:")
    print("   • https://www.kutrrh.go.ke")
    print("   • https://www.kutrrh.go.ke/about")
    print("   • https://www.kutrrh.go.ke/departments")
    print("   • https://www.kutrrh.go.ke/services")
    
    print("\n🔨 Building knowledge base...")
    print("   (This may take 30-70 seconds on first run)\n")
    
    # Initialize the knowledge base
    success = setup_hospital_knowledge_base()
    
    if success:
        print("\n✅ SUCCESS! Hospital knowledge base initialized.\n")
        print("📊 Knowledge Base Status:")
        print("   • Vector store: hospital_vector_store/")
        print("   • Status: Ready for queries")
        print("   • PDFs loaded: " + str(len(pdf_files)))
        print("   • Website content: Scraped")
        print("\n🎉 The hospital assistant is ready to answer questions!")
        print("\nYou can now:")
        print("   1. Run: streamlit run app.py")
        print("   2. Ask: 'What services do you provide?'")
        print("   3. Ask: 'What are your visiting hours?'")
        print("   4. Book: 'I'd like to schedule an appointment'\n")
        return True
    else:
        print("\n⚠️  Knowledge base setup completed with warnings.")
        print("   Check the logs above for details.")
        print("   The system may still work for appointment booking.")
        return False


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        logger.exception("Error during knowledge base initialization")
        sys.exit(1)
