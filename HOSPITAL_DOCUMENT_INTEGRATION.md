# Hospital Document Retrieval Integration Guide

## Overview
This guide explains how to integrate the hospital document retrieval system into your AI hospital booking assistant. The system uses Retrieval-Augmented Generation (RAG) to answer questions about hospital services, departments, contact information, and other details from PDF documents and the hospital website.

## Components Added

### 1. **hospital_retriever.py**
Core module for document retrieval:
- `HospitalDocumentRetriever` class: Manages PDF loading, website scraping, and vector store creation
- Uses FAISS for semantic search with HuggingFace embeddings
- Automatically chunks documents for better retrieval
- Supports local caching of vector stores

### 2. **hospital_tools.py**
LangChain integration tool:
- `search_hospital_information()` tool: Main function called by the agent
- `initialize_hospital_knowledge_base()`: Setup function
- Integrates seamlessly with the existing agent architecture

### 3. **hospital_setup.py**
Setup and initialization module:
- `setup_hospital_knowledge_base()`: Scans for PDFs and initializes knowledge base
- `DEFAULT_HOSPITAL_CONFIG`: Configuration for Kenyatta University Hospital
- Creates vector store from PDFs in `hospital_docs/` directory

### 4. **Updated Files**
- `agent.py`: Added `search_hospital_information` tool to agent's tools list
- `settings.yaml`: Enhanced system prompt with hospital information tool
- `app.py`: Initialize knowledge base on app startup
- `requirements.txt`: Added necessary dependencies (FAISS, sentence-transformers, PyPDF2, beautifulsoup4, etc.)

## Setup Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

The following new packages will be installed:
- `PyPDF2` - PDF text extraction
- `pdf2image` - PDF image processing
- `faiss-cpu` - Vector similarity search
- `sentence-transformers` - Embedding models
- `beautifulsoup4` - Website scraping
- `requests` - HTTP requests

### Step 2: Prepare Hospital Documents

Create a `hospital_docs/` directory in the project root and add hospital PDF files:

```
your-project/
├── hospital_docs/
│   ├── hospital_services.pdf
│   ├── departments_info.pdf
│   ├── contact_information.pdf
│   ├── visiting_hours.pdf
│   └── insurance_billing.pdf
├── app.py
├── agent.py
└── ...
```

### Step 3: Configure Hospital Website URLs (Optional)

Edit `hospital_setup.py` to add hospital website URLs:

```python
DEFAULT_HOSPITAL_CONFIG = {
    "hospital_name": "Kenyatta University Teaching Referral and Research Hospital",
    "website_urls": [
        "https://www.kutrrh.go.ke",
        "https://www.kutrrh.go.ke/departments",
        "https://www.kutrrh.go.ke/services",
        "https://www.kutrrh.go.ke/contact",
    ],
    "pdf_directory": "hospital_docs"
}
```

### Step 4: Run the Application

The knowledge base will be automatically initialized when the app starts:

```bash
streamlit run app.py
```

On first run:
1. The system will scan the `hospital_docs/` directory for PDFs
2. PDFs will be loaded and chunked
3. Embeddings will be created using HuggingFace's model
4. A FAISS vector store will be built and saved as `hospital_vector_store/`

## How It Works

### User Query Flow

1. **User asks about hospital information**
   - "What are your visiting hours?"
   - "What departments do you have?"
   - "How do I contact the hospital?"

2. **Agent detects it's a hospital information question**
   - Uses the `search_hospital_information()` tool

3. **Document Retrieval Process**
   - Query is converted to embeddings
   - FAISS performs semantic search in the vector store
   - Top 4 most relevant document chunks are retrieved
   - Retrieved documents are formatted with source information

4. **Response Generation**
   - Retrieved context is presented to the user
   - Information is attributed to source documents
   - User is advised to contact hospital for specific inquiries

### Key Features

- **Semantic Search**: Uses neural embeddings to find contextually relevant information
- **Multi-Source**: Combines PDFs and website content
- **Caching**: Vector store is cached locally for fast startup
- **Source Attribution**: All retrieved information includes source references
- **Graceful Degradation**: If knowledge base isn't available, tool provides helpful guidance

## Document Preparation Tips

### PDF Quality
- Use high-quality PDFs with good text extraction
- Avoid scanned images without OCR
- Organize PDFs by topic (services, departments, contact, etc.)

### Content Organization
Recommended document structure:
- **hospital_services.pdf**: Overview of hospital services and specialties
- **departments_info.pdf**: Department details, staff, services
- **contact_information.pdf**: Phone numbers, addresses, emails
- **visiting_hours.pdf**: Visiting hours, appointment scheduling info
- **insurance_billing.pdf**: Insurance details, payment methods, billing info
- **patient_information.pdf**: Patient rights, admission process, policies

### Website Content
The system can scrape website content, but ensure:
- Website is publicly accessible
- Page load times are reasonable
- Content is well-structured HTML

## Advanced Configuration

### Custom Embedding Model
To use a different embedding model in `hospital_retriever.py`:

```python
retriever = HospitalDocumentRetriever(
    embedding_model="sentence-transformers/all-mpnet-base-v2"
)
```

Available models:
- `all-MiniLM-L6-v2` (default, fast, good quality)
- `all-mpnet-base-v2` (better quality, slower)
- `paraphrase-MiniLM-L6-v2` (specialized for paraphrasing)

### Chunk Size Adjustment
Modify chunk size in `hospital_setup.py`:

```python
def setup_hospital_knowledge_base(
    pdf_directory: str = "hospital_docs",
    website_urls: Optional[List[str]] = None,
    chunk_size: int = 1500,  # Larger for longer documents
    chunk_overlap: int = 300  # More overlap for context
):
```

### Number of Retrieved Documents
Adjust in `hospital_tools.py`:

```python
retrieved_docs = retriever.retrieve_documents(query, k=6)  # Return top 6 instead of 4
```

## Troubleshooting

### Knowledge Base Not Loading
1. Check `hospital_docs/` directory exists
2. Verify PDF files are readable
3. Check logs for error messages: `logger.py` output
4. Ensure all dependencies are installed

### Slow Embeddings
- This is normal on first run
- Embeddings are cached after first load
- Consider using `all-MiniLM-L6-v2` model (default, fastest)

### Poor Retrieval Results
1. Ensure PDFs have good text extraction
2. Check document chunking isn't too small
3. Use multiple PDFs covering the same topic
4. Website URLs may need manual cleanup

### Memory Issues with Large PDFs
- Break large PDFs into smaller files
- Reduce chunk size
- Use lighter embedding models
- Consider incremental loading

## Testing the Integration

### Manual Test
Create a test script `test_hospital_retriever.py`:

```python
from hospital_setup import setup_hospital_knowledge_base
from hospital_tools import search_hospital_information

# Setup
setup_hospital_knowledge_base()

# Test queries
queries = [
    "What are your hospital visiting hours?",
    "What departments do you have?",
    "How do I contact the hospital?",
    "What is the address of the hospital?"
]

for query in queries:
    result = search_hospital_information(query)
    print(f"\nQuery: {query}")
    print(f"Answer: {result}\n")
```

## Production Considerations

1. **Vector Store Persistence**: Store `hospital_vector_store/` in stable location
2. **Regular Updates**: Rebuild vector store when hospital documents change
3. **Monitoring**: Log all retrieved documents and user queries
4. **Backup**: Keep backups of PDFs and vector store
5. **Cache Management**: Periodically clean up old vector stores

## Integration with Existing Features

The hospital information retrieval tool integrates seamlessly with:
- **Appointment Booking**: Users can ask about services before booking
- **Wait Time Predictions**: Users can learn about departments before selecting
- **Hospital Information**: Direct answers to patient questions

Example conversation flow:
```
Patient: "What departments do you have?"
Assistant: [Searches hospital info] "We have Cardiology, Orthopedics, General Surgery..."

Patient: "I'd like to book a cardiology appointment"
Assistant: [Switches to appointment tool] "I'll help you book that. First, I need your patient information..."
```

## Future Enhancements

Potential improvements:
- Add vector store versioning
- Implement document metadata filtering
- Add multi-language support
- Create admin UI for document management
- Add user query logging for optimization
- Implement feedback loop for retrieval quality

## Support

For issues or questions:
1. Check logs in the terminal output
2. Review the troubleshooting section
3. Verify dependencies with `pip list`
4. Test with sample PDFs first
5. Check hospital document formatting
