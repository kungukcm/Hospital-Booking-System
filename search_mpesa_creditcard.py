"""Search for MPESA and Credit Card in Service Charter"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Search specifically for MPESA and Credit Card
queries = [
    "Credit Cards MPESA paybill payment",
    "All payments shall be made through",
    "Credit Card or MPESA",
    "paybill numbers service points"
]

print("\nSearching for payment methods text:\n" + "="*70)

for query in queries:
    print(f"\nQuery: '{query}'")
    results = vector_store.similarity_search_with_score(query, k=3)
    
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        
        marker = " *** SERVICE CHARTER ***" if "Service-Charter" in source else ""
        
        print(f"\n{i}. Score: {score:.4f} | {os.path.basename(source)} (Page {page}){marker}")
        
        # Print full content for Service Charter results
        if "Service-Charter" in source:
            print(f"   FULL CONTENT:")
            print(f"   {doc.page_content}")
        else:
            snippet = doc.page_content[:150].replace('\n', ' ')
            print(f"   Snippet: {snippet}...")
