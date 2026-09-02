"""Test what exact response the LLM returns"""
import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("hospital_vector_store", embeddings, allow_dangerous_deserialization=True)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
synthesis_llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)

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

context_parts = []
sources_dict = {}

for i, (doc, score, search_query) in enumerate(all_results[:10]):
    source = doc.metadata.get("source", "Unknown")
    page = doc.metadata.get("page", "N/A")
    content = doc.page_content.strip()
    content = " ".join(content.split())
    
    if content:
        context_parts.append(f"Passage {i+1} (from {source}, Page {page}):\n{content}\n")
        if source not in sources_dict:
            sources_dict[source] = page

context = "\n".join(context_parts)

# Test the CURRENT prompt
extraction_prompt = ChatPromptTemplate.from_template("""You are a hospital information specialist. 
Extract the EXACT answer to the user's question from the hospital documents provided.

CRITICAL INSTRUCTIONS FOR PAYMENT METHODS QUESTIONS:
- When asked about payment methods, ALWAYS look for passages containing "Disclaimer", "All payments shall be made through", "Credit Card", or "MPESA"
- These are the PRIMARY answers to payment method questions
- Extract the EXACT phrase, word-for-word from the documents
- Do NOT use service tariffs (e.g., "Ksh 700", "Within 10 minutes") as the payment methods answer

GENERAL RULES:
1. Extract ONLY the relevant information, no extra details
2. Use EXACT text from the documents, don't paraphrase
3. Be concise and direct
4. If the specific information is not in the documents, say so clearly
5. For times/hours, extract exact times only
6. For contact, extract only phone numbers and emails
7. For services, extract only the service names and brief descriptions
8. For payment/tariff amounts, extract exact amounts and procedures

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
print("CURRENT RESPONSE:")
print("="*70)
print(answer)
print("="*70)
