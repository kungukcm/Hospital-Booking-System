import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Set HF_HUB_DISABLE_SYMLINKS_WARNING
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Test payment query with expansion like the tool does
test_queries = [
    "What are the payment methods?",
    # Expanded queries from improved version
    "NHIF insurance deposit admission payment",
    "hospital deposit Ksh payment",
    "payment proof of payment cost",
    "cash payment insurance authorization",
    "admission pack deposit general ward"
]

print("\nTesting improved query expansion for payment methods:\n" + "="*60)

for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = vector_store.similarity_search_with_score(query, k=3)
    
    for i, (doc, score) in enumerate(results, 1):
        source = doc.metadata.get('source', 'Unknown')
        page = doc.metadata.get('page', 'N/A')
        snippet = doc.page_content[:100].replace('\n', ' ')
        
        # Mark Service Charter results
        marker = " *** SERVICE CHARTER ***" if "Service-Charter" in source else ""
        
        print(f"{i}. Score: {score:.4f} | {os.path.basename(source)} (Page {page}){marker}")
        print(f"   Snippet: {snippet}...")
