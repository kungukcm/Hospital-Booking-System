"""
Hospital Knowledge Base Setup
Initializes the hospital documentation system with PDFs and website content
"""

import os
from typing import List, Optional
from hospital_tools import initialize_hospital_knowledge_base
from logger import setup_logger

logger = setup_logger(__name__)


def setup_hospital_knowledge_base(
    pdf_directory: str = "hospital_docs",
    website_urls: Optional[List[str]] = None,
    force_rebuild: bool = False
) -> bool:
    """
    Setup the hospital knowledge base with PDFs and website content
    
    Args:
        pdf_directory: Directory containing hospital PDF documents
        website_urls: List of hospital website URLs to scrape
        force_rebuild: Force rebuild even if vector store exists
        
    Returns:
        True if setup successful
    """
    try:
        logger.info("Setting up hospital knowledge base...")
        
        # Check if vector store already exists and is valid
        vector_store_path = "hospital_vector_store"
        if os.path.exists(vector_store_path) and not force_rebuild:
            # Check if the vector store has the required index files
            if os.path.exists(os.path.join(vector_store_path, "index.faiss")):
                logger.info("Valid vector store found - skipping rebuild")
                return True
        
        pdf_paths = []
        
        # Collect PDF files from directory
        if os.path.exists(pdf_directory):
            for filename in os.listdir(pdf_directory):
                if filename.lower().endswith('.pdf'):
                    pdf_path = os.path.join(pdf_directory, filename)
                    pdf_paths.append(pdf_path)
                    logger.info(f"Found PDF: {filename}")
        else:
            logger.warning(f"PDF directory not found: {pdf_directory}")
        
        # Default hospital website URLs for Kenyatta University Teaching Hospital
        if website_urls is None:
            website_urls = [
                "https://www.kutrrh.go.ke",  # Main hospital website
                "https://www.kutrrh.go.ke/about",
                "https://www.kutrrh.go.ke/departments",
                "https://www.kutrrh.go.ke/services",
            ]
        
        # Initialize knowledge base with PDFs and websites
        # (Websites are already in the vector store from rebuild_with_selenium.py, so this is primarily for PDFs)
        if pdf_paths or website_urls:
            logger.info(f"Initializing with {len(pdf_paths)} PDFs and {len(website_urls)} website URLs")
            success = initialize_hospital_knowledge_base(
                pdf_paths=pdf_paths if pdf_paths else None,
                website_urls=website_urls  # Will be used if vector store doesn't exist
            )
            
            if success:
                logger.info("Hospital knowledge base setup successful")
                return True
            else:
                logger.warning("Hospital knowledge base setup had issues but continuing...")
                return False
        else:
            logger.warning("No PDFs or website URLs available for knowledge base")
            return False
            
    except Exception as e:
        logger.error(f"Error setting up hospital knowledge base: {str(e)}")
        return False


def add_custom_hospital_documents(pdf_paths: List[str], website_urls: Optional[List[str]] = None) -> bool:
    """
    Add custom hospital documents to the knowledge base
    
    Args:
        pdf_paths: List of PDF file paths
        website_urls: List of website URLs
        
    Returns:
        True if addition successful
    """
    try:
        logger.info(f"Adding {len(pdf_paths)} custom PDFs to knowledge base")
        return initialize_hospital_knowledge_base(
            pdf_paths=pdf_paths,
            website_urls=website_urls
        )
    except Exception as e:
        logger.error(f"Error adding custom documents: {str(e)}")
        return False


# Sample configuration for Kenyatta University Hospital
DEFAULT_HOSPITAL_CONFIG = {
    "hospital_name": "Kenyatta University Teaching Referral and Research Hospital",
    "hospital_code": "KUTRRH",
    "website_urls": [
        "https://www.kutrrh.go.ke",
        "https://www.kutrrh.go.ke/departments",
        "https://www.kutrrh.go.ke/services",
        "https://www.kutrrh.go.ke/contact",
    ],
    "pdf_directory": "hospital_docs"
}
