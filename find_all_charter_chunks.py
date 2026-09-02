"""Find ALL Service Charter chunks in results"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Expanded queries from hospital_tools.py
queries = [
    "What are the payment methods?",
    "Credit Cards MPESA paybill payment",
    "All payments shall be made through",
    "hospital deposit Ksh payment",
    "NHIF insurance deposit admission",
    "cash payment insurance authorization",
    "admission pack deposit general ward"
]

print("\nSearching for ALL Service Charter results:\n" + "="*70)

all_charter_results = []

for query in queries:
    results = vector_store.similarity_search_with_score(query, k=10)
    for doc, score in results:
        source = doc.metadata.get('source', '')
        if "Service-Charter" in source:
            page = doc.metadata.get('page', 'N/A')
            all_charter_results.append({
                'query': query,
                'score': score,
                'page': page,
                'content': doc.page_content
            })

# Sort by score
all_charter_results.sort(key=lambda x: x['score'])

print(f"\nFound {len(all_charter_results)} Service Charter chunks total")
print("\nService Charter results (sorted by score):\n")

for i, result in enumerate(all_charter_results[:15], 1):
    print(f"{i}. Score: {result['score']:.4f} | Page {result['page']}")
    print(f"   Query: '{result['query']}'")
    print(f"   Content: {result['content'][:200]}")
    
    # Check if this is the payment methods chunk
    if "Credit Card" in result['content'] or "MPESA" in result['content']:
        print(f"   *** THIS IS THE PAYMENT METHODS CHUNK ***")
    print()
