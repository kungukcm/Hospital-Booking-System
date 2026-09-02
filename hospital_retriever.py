"""
Hospital Knowledge Base Retriever
Retrieves information from hospital PDFs and website content
"""

import os
import json
from typing import List, Tuple, Optional

try:
    from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_core.documents import Document
except ImportError as e:
    print(f"Warning: Some LangChain dependencies not available: {e}")
    Document = dict

from logger import setup_logger

logger = setup_logger(__name__)


class HospitalDocumentRetriever:
    """
    Manages document retrieval from hospital PDFs and website.
    Uses FAISS vector store for semantic search.
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the document retriever
        
        Args:
            embedding_model: HuggingFace embedding model to use
        """
        self.embedding_model = embedding_model
        try:
            import sentence_transformers
        except ImportError:
            logger.error("sentence_transformers not installed. Installing it now...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sentence-transformers'])
            import sentence_transformers
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
        self.documents = []
        logger.info(f"Initialized retriever with embedding model: {embedding_model}")
    
    def load_pdf_documents(self, pdf_paths: List[str]) -> List[Document]:
        """
        Load documents from PDF files
        
        Args:
            pdf_paths: List of paths to PDF files
            
        Returns:
            List of loaded documents
        """
        documents = []
        for pdf_path in pdf_paths:
            try:
                if not os.path.exists(pdf_path):
                    logger.warning(f"PDF file not found: {pdf_path}")
                    continue
                
                logger.info(f"Loading PDF: {pdf_path}")
                loader = PyPDFLoader(pdf_path)
                pdf_docs = loader.load()
                documents.extend(pdf_docs)
                logger.info(f"Loaded {len(pdf_docs)} pages from {pdf_path}")
            except Exception as e:
                logger.error(f"Error loading PDF {pdf_path}: {str(e)}")
        
        return documents
    
    def load_website_content(self, website_urls: List[str]) -> List[Document]:
        """
        Load content from hospital website URLs
        Uses Selenium for JavaScript-rendered pages (board, executive, directorates)
        
        Args:
            website_urls: List of hospital website URLs
            
        Returns:
            List of loaded documents
        """
        import requests
        from bs4 import BeautifulSoup
        
        # Pages that need JavaScript rendering
        js_pages = ['board-of-directors', 'the-executive', 'directorates']
        
        documents = []
        for url in website_urls:
            try:
                logger.info(f"Loading website content from: {url}")
                
                # Use Selenium for JavaScript-heavy pages
                if any(page in url for page in js_pages):
                    text = self._load_with_selenium(url)
                else:
                    # Use requests for static pages
                    response = requests.get(url, timeout=10, verify=False)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    text = soup.get_text(separator='\n', strip=True)
                
                if text.strip():
                    doc = Document(page_content=text, metadata={"source": url})
                    documents.append(doc)
                    logger.info(f"Loaded content from {url}")
                else:
                    logger.warning(f"No text content extracted from {url}")
            except Exception as e:
                logger.warning(f"Error loading website {url}: {str(e)}")
        
        return documents
    
    def _load_with_selenium(self, url: str) -> str:
        """
        Load JavaScript-rendered page content using Selenium
        
        Args:
            url: Website URL to load
            
        Returns:
            Extracted text content
        """
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        
        driver = None
        try:
            # Initialize Chrome driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Load the page
            driver.get(url)
            
            # Wait for content to load (adjust selector based on page structure)
            wait = WebDriverWait(driver, 10)
            time.sleep(3)  # Additional wait for dynamic content
            
            # Extract text from body
            text = driver.find_element(By.TAG_NAME, 'body').text
            
            return text
            
        except Exception as e:
            logger.error(f"Selenium error loading {url}: {str(e)}")
            return ""
        finally:
            if driver:
                driver.quit()
    
    def chunk_documents(self, documents: List[Document],
                       chunk_size: int = 500,  # Tighter chunks to keep names with titles
                       chunk_overlap: int = 100) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval
        Preserves metadata including source and page numbers
        Uses specific separators to keep related information together
        
        Args:
            documents: List of documents to chunk
            chunk_size: Size of each chunk (500 chars to keep leadership details intact)
            chunk_overlap: Overlap between chunks (100 for context continuity)
            
        Returns:
            List of chunked documents with preserved metadata
        """
        logger.info(f"Chunking {len(documents)} documents with size {chunk_size}")
        
        # Use more specific separators to keep information together
        # Website content often has patterns like "Visiting Hours" followed by times
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\nVisiting",  # Keep visiting hours together
                "\nContact",   # Keep contact info together
                "\nServices",  # Keep services together
                "\nPayment",   # Keep payment info together
                "\n\n",       # Paragraph breaks
                "\n",         # Line breaks
                " ",          # Word breaks
                ""            # Character breaks
            ]
        )
        
        chunked_docs = text_splitter.split_documents(documents)
        
        # Ensure all chunks retain their source metadata
        for doc in chunked_docs:
            if "source" not in doc.metadata and len(documents) > 0:
                # Try to match with original document's source
                doc.metadata["source"] = documents[0].metadata.get("source", "Unknown")
        
        logger.info(f"Created {len(chunked_docs)} chunks from {len(documents)} documents")
        
        return chunked_docs
    
    def build_vector_store(self, documents: List[Document], 
                          vectorstore_path: str = "hospital_vector_store") -> None:
        """
        Build FAISS vector store from documents
        
        Args:
            documents: List of documents to index
            vectorstore_path: Path to save/load vector store
        """
        try:
            # Check if vector store already exists
            if os.path.exists(vectorstore_path):
                logger.info(f"Loading existing vector store from {vectorstore_path}")
                self.vector_store = FAISS.load_local(
                    vectorstore_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                self.documents = documents
                logger.info(f"Vector store loaded with {len(documents)} documents")
                return
            
            if not documents:
                logger.warning("No documents provided to build vector store")
                return
            
            logger.info(f"Building new vector store with {len(documents)} documents")
            self.vector_store = FAISS.from_documents(
                documents,
                self.embeddings
            )
            self.documents = documents
            
            # Save the vector store
            self.vector_store.save_local(vectorstore_path)
            logger.info(f"Vector store saved to {vectorstore_path}")
            
        except Exception as e:
            logger.error(f"Error building vector store: {str(e)}")
            raise
    
    def retrieve_documents(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """
        Retrieve most relevant documents for a query
        
        Args:
            query: User query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, similarity_score) tuples
        """
        if not self.vector_store:
            logger.warning("Vector store not initialized")
            return []
        
        try:
            logger.info(f"Retrieving {k} documents for query: {query}")
            results = self.vector_store.similarity_search_with_score(query, k=k)
            logger.info(f"Retrieved {len(results)} documents")
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []
    
    def format_context(self, retrieved_docs: List[Tuple[Document, float]], 
                      max_tokens: int = 1500) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            retrieved_docs: List of retrieved documents with scores
            max_tokens: Maximum tokens in context
            
        Returns:
            Formatted context string
        """
        context_parts = []
        token_count = 0
        
        for doc, score in retrieved_docs:
            content = doc.page_content
            # Estimate tokens (rough: 4 chars per token)
            tokens = len(content) / 4
            
            if token_count + tokens > max_tokens:
                break
            
            context_parts.append(f"[Source: {doc.metadata.get('source', 'Unknown')}]\n{content}")
            token_count += tokens
        
        return "\n\n---\n\n".join(context_parts)
    
    def initialize_hospital_knowledge_base(self, 
                                          pdf_paths: Optional[List[str]] = None,
                                          website_urls: Optional[List[str]] = None,
                                          vectorstore_path: str = "hospital_vector_store") -> bool:
        """
        Initialize the complete hospital knowledge base
        
        Args:
            pdf_paths: List of PDF file paths
            website_urls: List of website URLs
            vectorstore_path: Path for vector store
            
        Returns:
            True if initialization successful
        """
        try:
            documents = []
            
            # Load PDFs
            if pdf_paths:
                pdf_docs = self.load_pdf_documents(pdf_paths)
                documents.extend(pdf_docs)
            
            # Load website content
            if website_urls:
                web_docs = self.load_website_content(website_urls)
                documents.extend(web_docs)
            
            if not documents:
                logger.warning("No documents loaded from PDFs or websites")
                return False
            
            # Chunk documents
            chunked_docs = self.chunk_documents(documents)
            
            # Build vector store
            self.build_vector_store(chunked_docs, vectorstore_path)
            
            logger.info("Hospital knowledge base initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing hospital knowledge base: {str(e)}")
            return False


def get_hospital_retriever() -> HospitalDocumentRetriever:
    """
    Get or create singleton hospital document retriever
    """
    return HospitalDocumentRetriever()
