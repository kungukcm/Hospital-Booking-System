"""Debug the search and LLM extraction"""
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
print(f"Expanded to: {len(expanded_queries)} queries")
print("\nRetrieving documents...\n")

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

# Prepare context from top 10
context_parts = []
sources_dict = {}

print("Top 10 results:")
print("="*70)

for i, (doc, score, search_query) in enumerate(all_results[:10]):
    source = doc.metadata.get("source", "Unknown")
    page = doc.metadata.get("page", "N/A")
    content = doc.page_content.strip()
    
    # Clean up content
    content = " ".join(content.split())
    
    marker = " *** SERVICE CHARTER ***" if "Service-Charter" in source else ""
    print(f"{i+1}. Score: {score:.4f} | {os.path.basename(source)}{marker}")
    print(f"   Query: '{search_query}'")
    print(f"   Content: {content[:100]}...\n")
    
    if content:
        context_parts.append(f"Passage {i+1} (from {source}, Page {page}):\n{content}\n")
        if source not in sources_dict:
            sources_dict[source] = page

context = "\n".join(context_parts)

print("\n" + "="*70)
print("Now sending to LLM for extraction...")
print("="*70 + "\n")

# Use LLM to extract answer
extraction_prompt = ChatPromptTemplate.from_template("""You are a hospital information specialist. 
Extract the EXACT answer to the user's question from the hospital documents provided.

IMPORTANT RULES:
1. Extract ONLY the relevant information, no extra details
2. Use EXACT text from the documents, don't paraphrase
3. Be concise and direct
4. If the information is not in the documents, say so clearly
5. For times/hours, extract exact times only
6. For contact, extract only phone numbers and emails
7. For services, extract only the service names and brief descriptions
8. For payment methods, look for terms like: Credit Card, MPESA, paybill, cash, bank transfer, payment modes, "payments shall be made through"
9. For payment/tariff, extract exact payment methods, amounts, and procedures from any passage that mentions payment or disclaimer

User Question: {question}

Hospital Document Passages:
{context}

Extract the EXACT answer (be concise):"""
)

chain = extraction_prompt | synthesis_llm
response = chain.invoke({
    "question": query,
    "context": context
})

answer = response.content.strip()
print(f"LLM Response:\n{answer}")
print("\n" + "="*70)
print(f"\nSources: {list(sources_dict.keys())}")
