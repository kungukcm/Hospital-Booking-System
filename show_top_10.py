"""Show which documents are in top 10"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

query = "What are the payment methods?"
expanded_queries = [query, "Credit Cards MPESA paybill payment", "All payments shall be made through", "hospital deposit Ksh payment", "NHIF insurance deposit admission", "cash payment insurance authorization", "admission pack deposit general ward"]

all_results = []
seen_content = set()

for search_query in expanded_queries:
    retrieved_docs = vector_store.similarity_search_with_score(search_query, k=5)
    for doc, score in retrieved_docs:
        content_hash = hash(doc.page_content[:100])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            all_results.append((doc, score, search_query))

all_results.sort(key=lambda x: x[1])

print("\nTop 10 results (sorted by score):")
print("="*80)

for i, (doc, score, sq) in enumerate(all_results[:10]):
    source = doc.metadata.get("source", "Unknown")
    content = doc.page_content[:100]
    has_payment = "Credit Card" in doc.page_content or "MPESA" in doc.page_content or "payments shall be made" in doc.page_content
    marker = " <<<< PAYMENT METHODS >>>>" if has_payment else ""
    
    print(f"\n{i+1}. Score: {score:.4f}{marker}")
    print(f"   Source: {os.path.basename(source)}")
    print(f"   Query: '{sq}'")
    try:
        print(f"   Content: {content}...")
    except:
        print(f"   Content: [Non-ASCII characters]")

print("\n" + "="*80)
print(f"\nPayment methods chunk is at position: {next((i+1 for i, (d, _, _) in enumerate(all_results) if 'Credit Card' in d.page_content), 'NOT FOUND')}")
