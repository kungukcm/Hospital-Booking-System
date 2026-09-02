# Hospital Document Retrieval System - Architecture & Setup Guide

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI (app.py)                    │
│  Patient asks question about hospital or wants to book appt    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LANGRAPH AGENT (agent.py)                     │
│  - Routes to appropriate tool based on question type           │
│  - Maintains conversation history                              │
│  - Synthesizes responses                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                                  │
        ▼                                  ▼
┌──────────────────────┐        ┌──────────────────────────────────┐
│  APPOINTMENT TOOLS   │        │  HOSPITAL INFO TOOL              │
│  (existing)          │        │  search_hospital_information()   │
│                      │        │  (hospital_tools.py)             │
│ - book_appointment   │        │                                  │
│ - cancel_appointment │        │ ▼ Routes to retriever            │
│ - get_wait_time      │        │                                  │
│ - etc.               │        └──────────────┬───────────────────┘
└──────────────────────┘                       │
                                               ▼
                                    ┌──────────────────────────────┐
                                    │ HOSPITAL RETRIEVER           │
                                    │ (hospital_retriever.py)      │
                                    │                              │
                                    │ 1. Query to embeddings       │
                                    │ 2. Search FAISS vector store │
                                    │ 3. Retrieve top 4 docs       │
                                    │ 4. Format with sources       │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────┴───────────────┐
                                    │                              │
                    ┌───────────────▼──────┐      ┌────────────────▼──┐
                    │ FAISS VECTOR STORE   │      │ CHUNK DOCUMENTS   │
                    │ hospital_vector_store/      │ + EMBEDDINGS      │
                    │                      │      │                   │
                    │ Semantic search      │      │ (Cached locally)  │
                    │ Fast retrieval       │      │                   │
                    │ Similarity scoring   │      │                   │
                    └──────────────────────┘      └─────────────────┬─┘
                                                                     │
                                    ┌────────────────────────────────┘
                                    │
                    ┌───────────────▼─────────┐
                    │ SOURCE DOCUMENTS        │
                    │                         │
                    ├─ hospital_docs/ PDFs    │
                    │   ├ services.pdf        │
                    │   ├ departments.pdf     │
                    │   ├ contact.pdf         │
                    │   ├ visiting_hours.pdf  │
                    │   └ insurance.pdf       │
                    │                         │
                    ├─ Hospital Website       │
                    │   ├ kutrrh.go.ke        │
                    │   ├ services page       │
                    │   └ contact page        │
                    └─────────────────────────┘
```

## Data Flow for Hospital Information Query

```
User: "What are your visiting hours?"
│
├─ Embedded in agent prompt context
├─ Current time: 2026-01-18 12:00
├─ Conversation history: [previous messages]
│
▼
Agent decision: "This is a hospital info question"
│
▼
search_hospital_information("What are your visiting hours?")
│
▼ Hospital Retriever
├─ Convert query to embeddings (sentence-transformers)
├─ Search vector store with FAISS
├─ Find 4 most relevant document chunks
│  (scores: 0.95, 0.87, 0.82, 0.71)
│
▼ Retrieved Documents
├─ Chunk 1: "Hospital visiting hours are 10 AM to 7 PM daily..."
│           (Source: hospital_docs/visiting_hours.pdf)
├─ Chunk 2: "Special visiting hours on weekends..."
│           (Source: hospital website)
├─ Chunk 3: "ICU visiting restrictions..."
│           (Source: hospital_docs/policies.pdf)
└─ Chunk 4: "Contact information for visitor info..."
            (Source: hospital website)
│
▼ Format Context
"Based on hospital documents, here's the information I found:

[Source: hospital_docs/visiting_hours.pdf]
Hospital visiting hours are 10 AM to 7 PM daily...

[Source: hospital website]
Special visiting hours on weekends...

[Source: hospital_docs/policies.pdf]
ICU visiting restrictions...

---

If you need more specific information, please contact the hospital directly."
│
▼
Agent synthesizes response:
"Our hospital visiting hours are 10 AM to 7 PM daily. We have special
weekend hours. For ICU patients, there are specific visiting restrictions.
Would you like more information about this or help with something else?"
```

## Component Interaction Diagram

```
┌──────────────┐
│  Settings    │ (settings.yaml)
│  & Config    │
└──────┬───────┘
       │ system_prompt + tool_descriptions
       │
       ▼
┌──────────────────────────┐
│  GROQ LLM                │ (llama-3.3-70b)
│  (Via LangChain)         │
└──────┬───────────────────┘
       │ generates tool calls
       │
       ▼
┌────────────────────────────┐
│  LangGraph Agent           │
│  (Workflow execution)      │
└──────┬─────────────────────┘
       │ orchestrates tools
       │
       ├─→ Tool Node (ToolNode)
       │   ├─ book_appointment
       │   ├─ cancel_appointment
       │   ├─ get_wait_time_prediction
       │   └─ search_hospital_information ◄─ NEW
       │
       ▼
┌────────────────────────────┐
│  Hospital Tools Module     │
│  (hospital_tools.py)       │
└──────┬─────────────────────┘
       │ calls retriever
       │
       ▼
┌────────────────────────────┐
│  Hospital Retriever        │
│  (hospital_retriever.py)   │
└──────┬─────────────────────┘
       │
       ├─ load_pdf_documents()
       ├─ load_website_content()
       ├─ chunk_documents()
       ├─ build_vector_store()
       └─ retrieve_documents()
           │
           ├─ HuggingFace Embeddings
           │  (all-MiniLM-L6-v2)
           │
           └─ FAISS Vector Store
              ├─ Similarity search
              └─ Top-k retrieval
```

## File Structure After Integration

```
your-project-root/
│
├── NEW: hospital_retriever.py      (Core RAG system)
├── NEW: hospital_tools.py          (Agent tool definition)
├── NEW: hospital_setup.py          (Setup & initialization)
├── NEW: hospital_examples.py       (Example code)
│
├── MODIFIED: agent.py              (Added hospital tool)
├── MODIFIED: app.py                (Init knowledge base)
├── MODIFIED: settings.yaml         (Enhanced prompt)
├── MODIFIED: requirements.txt      (New dependencies)
│
├── NEW: HOSPITAL_INTEGRATION_SUMMARY.md
├── NEW: HOSPITAL_DOCUMENT_INTEGRATION.md
├── NEW: HOSPITAL_DOCS_QUICKSTART.md
│
├── hospital_docs/                  (Create this folder)
│   ├── services.pdf               (Add your hospital PDFs)
│   ├── departments.pdf
│   ├── contact_information.pdf
│   ├── visiting_hours.pdf
│   └── insurance_billing.pdf
│
├── hospital_vector_store/          (Auto-created on first run)
│   ├── index.faiss
│   ├── index.pkl
│   └── docstore.pkl
│
├── data/
│   └── appointments.json
│
├── models/
│   ├── scaler_X.joblib
│   ├── tcn_scheduling_model.h5
│   └── y_scaler.joblib
│
├── app.py
├── agent.py
├── config.py
├── constants.py
├── logger.py
├── appointments_db.py
├── appointment_recommender.py
├── enhanced_tools.py
├── tools.py
├── utils.py
├── requirements.txt
├── settings.yaml
├── Dockerfile
├── docker-compose.yml
├── README.md
└── [other files...]
```

## Initialization Flow

```
1. App Start (streamlit run app.py)
   │
   ├─ Load config.py
   ├─ Initialize logger
   ├─ Set up session state
   │  └─ IF 'initialized' not in session:
   │     └─ Call: setup_hospital_knowledge_base()
   │
   ▼
2. Hospital Setup (hospital_setup.py)
   │
   ├─ Check if hospital_docs/ exists
   ├─ Scan for PDF files
   ├─ Get configured website URLs
   │
   ▼
3. Knowledge Base Build (hospital_retriever.py)
   │
   ├─ Load PDFs from hospital_docs/
   │  └─ Extract text from each PDF
   │
   ├─ Load website content (if URLs provided)
   │  └─ Scrape and clean HTML
   │
   ├─ Chunk documents
   │  └─ Split into 1000-char chunks with 200-char overlap
   │
   ├─ Create embeddings
   │  └─ Convert each chunk to vector (sentence-transformers)
   │
   ├─ Build FAISS index
   │  └─ Create searchable vector store
   │
   ├─ Save to disk
   │  └─ hospital_vector_store/ folder
   │
   └─ DONE - Ready for queries!

Subsequent runs:
   ├─ Detect hospital_vector_store/ exists
   ├─ Load cached vector store
   ├─ INSTANT - Ready for queries!
```

## Query Processing Steps

```
User Message: "What departments do you have?"
│
▼ Step 1: Agent Analysis
├─ Parse user intent
├─ Check conversation history
├─ Determine if appointment or info question
│
▼ Step 2: Tool Selection
├─ Agent decides: "This is hospital info"
├─ Selects: search_hospital_information()
│
▼ Step 3: Retrieval
├─ Convert query to embedding (512-dimensional vector)
├─ Search FAISS vector store
├─ Get 4 most similar document chunks
│  └─ Score: [0.95, 0.87, 0.82, 0.71]
│
▼ Step 4: Formatting
├─ Extract source information
├─ Format retrieved text with sources
├─ Limit to ~1500 tokens
│
▼ Step 5: LLM Response
├─ Pass context to LLM
├─ LLM generates natural response
│
▼ Final Response:
"Based on our hospital documents, we have:
- Cardiology
- Orthopedics
- General Surgery
- Pediatrics
- Neurology
- ...

For more information about specific departments,
please contact us at [contact info]"
```

## Performance Characteristics

```
First Run (Knowledge Base Build):
├─ PDF Loading: 2-5 seconds
├─ Text Extraction: 5-15 seconds
├─ Document Chunking: 1-2 seconds
├─ Embeddings Creation: 20-45 seconds (main bottleneck)
├─ Vector Store Build: 2-3 seconds
├─ Save to Disk: 1-2 seconds
│
└─ Total: ~35-70 seconds

Subsequent Runs:
├─ Load Vector Store: <100 milliseconds
│
└─ Total: Instant!

Per Query:
├─ Embedding Query: 100-200 milliseconds
├─ FAISS Search: 10-50 milliseconds
├─ LLM Generation: 1-3 seconds
│
└─ Total Response Time: 1.5-3.5 seconds
```

## Dependencies Overview

```
New packages added to requirements.txt:

Core RAG:
├─ faiss-cpu          (Vector similarity search)
└─ sentence-transformers  (Neural embeddings)

PDF Processing:
├─ PyPDF2             (PDF text extraction)
└─ pdf2image          (PDF image conversion)

Web Scraping:
├─ beautifulsoup4     (HTML parsing)
└─ requests           (HTTP requests)

Note: These integrate with existing:
├─ langchain          (LLM framework)
├─ langchain_community (Document loaders)
└─ langchain_core     (Base types)
```

---

This integration enables your hospital booking system to become an **intelligent hospital assistant** that can both answer questions about hospital services AND book appointments with AI-powered optimization.
