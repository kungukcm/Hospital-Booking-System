#!/usr/bin/env python3
"""Check what CEO/leadership data is in the knowledge base"""

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from logger import setup_logger

logger = setup_logger(__name__)

store_path = 'hospital_vector_store'

if os.path.exists(store_path):
    print('Vector store exists. Checking contents...')
    
    embeddings = HuggingFaceEmbeddings(
        model_name='all-MiniLM-L6-v2',
        encode_kwargs={'normalize_embeddings': True}
    )
    
    try:
        vector_store = FAISS.load_local(store_path, embeddings, allow_dangerous_deserialization=True)
        
        # Search for CEO information
        queries = ['CEO', 'chief executive', 'leadership', 'management', 'director']
        
        for query in queries:
            print(f'\n=== Searching for: "{query}" ===')
            results = vector_store.similarity_search(query, k=5)
            
            print(f'Found {len(results)} documents:')
            for i, doc in enumerate(results):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                content = doc.page_content[:300]
                print(f'\n{i+1}. Source: {source} | Page: {page}')
                print(f'   Content: {content}...')
                
    except Exception as e:
        print(f'Error loading vector store: {e}')
        import traceback
        traceback.print_exc()
else:
    print(f'Vector store does not exist at {store_path}')
    print('Run: python initialize_knowledge_base.py')
