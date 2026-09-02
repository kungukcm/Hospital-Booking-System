from hospital_retriever import HospitalDocumentRetriever
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize retriever and load vector store
retriever = HospitalDocumentRetriever()
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    encode_kwargs={'normalize_embeddings': True}
)
retriever.vector_store = FAISS.load_local(
    "hospital_vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)

print("Testing payment method queries...\n")

queries = [
    "What are the payment methods?",
    "How do I pay at KUTRRH?",
    "payment deposit admission",
    "NHIF insurance payment",
    "hospital payment options"
]

for query in queries:
    print(f"\nQuery: {query}")
    print("="*80)
    results = retriever.retrieve_documents(query, k=3)
    
    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        content_preview = doc.page_content[:200].replace('\n', ' ')
        print(f"\n{i+1}. Score: {score:.4f}")
        print(f"   Source: {source} (Page {page})")
        print(f"   Content: {content_preview}...")
