#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify hospital knowledge base is working
"""

import os
import sys
import io

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import warnings
warnings.filterwarnings('ignore')

def test_knowledge_base():
    """Test the hospital knowledge base initialization and retrieval"""
    print("\n" + "="*60)
    print("🏥 Hospital Knowledge Base Test")
    print("="*60 + "\n")
    
    try:
        from hospital_tools import get_hospital_retriever
        from hospital_setup import setup_hospital_knowledge_base
        from hospital_retriever import HospitalDocumentRetriever
        
        print("✅ Hospital modules imported successfully\n")
        
        # Check if vector store exists
        vector_store_path = "hospital_vector_store"
        if os.path.exists(vector_store_path):
            print(f"✅ Vector store found at: {vector_store_path}")
            print(f"   Size: {sum(os.path.getsize(f) for f in os.listdir(vector_store_path) for f in [os.path.join(vector_store_path, f)] if os.path.isfile(f)) / (1024*1024):.2f} MB")
        else:
            print(f"❌ Vector store not found at: {vector_store_path}")
            print("   Initializing now...")
            setup_hospital_knowledge_base()
            print("✅ Vector store created successfully!")
        
        print("\n📚 Testing retrieval with sample queries:\n")
        
        # Test queries
        test_queries = [
            "What is the hospital about?",
            "What services do you provide?",
            "What are the contact details?"
        ]
        
        retriever = get_hospital_retriever()
        
        for i, query in enumerate(test_queries, 1):
            print(f"{i}. Query: '{query}'")
            try:
                # Use the retriever directly (not the tool wrapper)
                result = retriever.retrieve_documents(query)
                print(f"   ✅ Response retrieved ({len(result)} results)")
                if result:
                    # Format the response
                    response_text = retriever.format_context(result)
                    print(f"   Preview: {response_text[:150]}...")
                else:
                    print("   ⚠️  No relevant information found")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
            print()
        
        print("="*60)
        print("✅ Knowledge Base Test Complete!")
        print("="*60)
        print("\nYou can now run: streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_knowledge_base()
