"""Debug the search and LLM extraction - fixed Unicode"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

print("Loading vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

# Initialize LLM
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
synthesis_llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)

# Simulate the query expansion from hospital_tools.py
query = "What are the payment methods?"
expanded_queries = [query]

if "payment" in query.lower():
    expanded_queries.extend([
        "Credit Cards MPESA paybill payment",
        "All payments shall be made through",
        "hospital deposit Ksh payment",
        "NHIF insurance deposit admission",
        "cash payment insurance authorization",
        "admission pack deposit general ward"
    ])

print(f"\nOriginal query: '{query}'")
print(f"Expanded to: {len(expanded_queries)} queries\n")

# Retrieve documents
all_results = []
seen_content = set()

for search_query in expanded_queries:
    retrieved_docs = vector_store.similarity_search_with_score(search_query, k=5)
    for doc, score in retrieved_docs:
        content_hash = hash(doc.page_content[:100])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            all_results.append((doc, score, search_query))

# Sort by score
all_results.sort(key=lambda x: x[1])

print(f"Retrieved {len(all_results)} unique documents\n")

# Show ALL Charter chunks
print("="*70)
print("ALL SERVICE CHARTER CHUNKS:")
print("="*70)

charter_chunks = [(doc, score, sq) for doc, score, sq in all_results if "Service-Charter" in doc.metadata.get("source", "")]
for i, (doc, score, sq) in enumerate(charter_chunks):
    marker = " *** PAYMENT METHODS ***" if "Credit Card" in doc.page_content or "MPESA" in doc.page_content else ""
    print(f"\n{i+1}. Score: {score:.4f} {marker}")
    print(f"   Query: '{sq}'")
    # Use ASCII only for display
    try:
        snippet = doc.page_content[:200]
        print(f"   Content: {snippet}")
    except:
        print(f"   Content: [Contains non-ASCII characters]")

print("\n" + "="*70)
print(f"Found {len(charter_chunks)} Service Charter chunks")
print("="*70)
