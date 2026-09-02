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

print("Searching for specific payment terms in vector store...\n")

queries = [
    "NHIF insurance deposit admission payment",
    "hospital deposit Ksh 2500",
    "identification documents payment deposit"
]

for query in queries:
    print(f"\nQuery: '{query}'")
    print("="*80)
    results = retriever.retrieve_documents(query, k=5)
    
    for i, (doc, score) in enumerate(results):
        source = doc.metadata.get("source", "Unknown").split("\\")[-1]
        page = doc.metadata.get("page", "N/A")
        
        # Check if this is the Service Charter
        is_charter = "Service-Charter" in source
        marker = " *** SERVICE CHARTER ***" if is_charter else ""
        
        print(f"\n{i+1}. Score: {score:.4f} | {source} (Page {page}){marker}")
        
        # Print snippet
        snippet = doc.page_content[:150].replace('\n', ' ').encode('ascii', 'ignore').decode('ascii')
        print(f"   Snippet: {snippet}...")
