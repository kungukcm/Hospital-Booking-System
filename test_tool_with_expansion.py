"""Test the hospital search tool with its query expansion logic"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Simulate the tool's query expansion logic
def expand_query(query):
    """Mimic the query expansion in hospital_tools.py"""
    queries = [query]
    query_lower = query.lower()
    
    if "payment" in query_lower or "cost" in query_lower or "price" in query_lower or "pay" in query_lower:
        queries.extend([
            "NHIF insurance deposit admission payment",
            "hospital deposit Ksh payment",
            "payment proof of payment cost",
            "cash payment insurance authorization",
            "admission pack deposit general ward"
        ])
    elif "visit" in query_lower or "hours" in query_lower:
        queries.extend([
            "visiting hours patients family",
            "visit time schedule",
            "visiting hours policy"
        ])
    elif "contact" in query_lower or "phone" in query_lower or "email" in query_lower:
        queries.extend([
            "telephone email contact details",
            "phone number address contact",
            "customer care helpline"
        ])
    
    return queries

# Test query
test_query = "What are the payment methods?"
print(f"\n{'='*70}")
print(f"Original query: '{test_query}'")
print(f"{'='*70}")

expanded = expand_query(test_query)
print(f"\nExpanded to {len(expanded)} queries:")
for i, q in enumerate(expanded, 1):
    print(f"  {i}. {q}")

# Get results for each expanded query
print(f"\n{'='*70}")
print("Results from each expanded query:")
print(f"{'='*70}")

all_results = {}
for query in expanded:
    results = vector_store.similarity_search_with_score(query, k=5)
    for doc, score in results:
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        key = f"{source}_{page}"
        
        # Keep best score for this document chunk
        if key not in all_results or score < all_results[key]['score']:
            all_results[key] = {
                'source': os.path.basename(source),
                'page': page,
                'score': score,
                'query': query,
                'content': doc.page_content[:150].replace('\n', ' ')
            }

# Sort by score and show top 8
sorted_results = sorted(all_results.values(), key=lambda x: x['score'])[:8]

print(f"\nTop 8 unique results after deduplication:")
for i, result in enumerate(sorted_results, 1):
    marker = " *** SERVICE CHARTER ***" if "Service-Charter" in result['source'] else ""
    print(f"\n{i}. Score: {result['score']:.4f} | {result['source']} (Page {result['page']}){marker}")
    print(f"   Retrieved by query: '{result['query']}'")
    # Use ASCII only for printing
    try:
        print(f"   Snippet: {result['content']}...")
    except UnicodeEncodeError:
        print(f"   Snippet: [Contains non-ASCII characters]")
