"""Test updated query expansion"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Mimic the NEW query expansion
def expand_query(query):
    queries = [query]
    query_lower = query.lower()
    
    if "payment" in query_lower or "cost" in query_lower or "price" in query_lower or "pay" in query_lower:
        queries.extend([
            "Credit Cards MPESA paybill payment",
            "All payments shall be made through",
            "hospital deposit Ksh payment",
            "NHIF insurance deposit admission",
            "cash payment insurance authorization",
            "admission pack deposit general ward"
        ])
    
    return queries

test_query = "What are the payment methods?"
print(f"\nOriginal query: '{test_query}'")

expanded = expand_query(test_query)
print(f"\nExpanded to {len(expanded)} queries")

# Get results for each expanded query
all_results = {}
for query in expanded:
    results = vector_store.similarity_search_with_score(query, k=5)
    for doc, score in results:
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        key = f"{source}_{page}_{doc.page_content[:50]}"
        
        if key not in all_results or score < all_results[key]['score']:
            all_results[key] = {
                'source': os.path.basename(source),
                'page': page,
                'score': score,
                'query': query,
                'content': doc.page_content
            }

# Sort by score and show top 8
sorted_results = sorted(all_results.values(), key=lambda x: x['score'])[:8]

print(f"\nTop 8 results after deduplication:")
for i, result in enumerate(sorted_results, 1):
    marker = " *** SERVICE CHARTER ***" if "Service-Charter" in result['source'] else ""
    print(f"\n{i}. Score: {result['score']:.4f} | {result['source']} (Page {result['page']}){marker}")
    print(f"   Retrieved by: '{result['query'][:60]}'")
    
    # Show content if it's Service Charter
    if "Service-Charter" in result['source']:
        print(f"   === CONTENT ===")
        print(f"   {result['content'][:300]}")
