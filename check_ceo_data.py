#!/usr/bin/env python3
"""Check what CEO data is in the vector store"""

from hospital_retriever import HospitalDocumentRetriever
import os

# Load the vector store
retriever = HospitalDocumentRetriever()
vector_store_path = os.path.join(os.path.dirname(__file__), "hospital_vector_store")

if os.path.exists(vector_store_path):
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
else:
    store = None

if store:
    print("=== Raw Vector Store Retrieval for CEO ===\n")
    
    # Query for CEO
    docs = store.similarity_search("Who is the CEO", k=5)
    
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', 'Unknown')
        content = doc.page_content[:300]
        print(f"{i}. Source: {source}")
        print(f"   Content: {content}...\n")
    
    # Also search for Zeinab Gura specifically
    print("\n=== Search for 'Zeinab Gura' ===\n")
    docs_zeinab = store.similarity_search("Zeinab Gura Chief Executive", k=3)
    for i, doc in enumerate(docs_zeinab, 1):
        source = doc.metadata.get('source', 'Unknown')
        content = doc.page_content[:300]
        print(f"{i}. Source: {source}")
        print(f"   Content: {content}...\n")
        
    # Search for Anthony Kamau
    print("\n=== Search for 'Anthony Kamau' ===\n")
    docs_anthony = store.similarity_search("Anthony Kamau Chief Executive", k=3)
    for i, doc in enumerate(docs_anthony, 1):
        source = doc.metadata.get('source', 'Unknown')
        content = doc.page_content[:300]
        print(f"{i}. Source: {source}")
        print(f"   Content: {content}...\n")
else:
    print("Vector store not found")
