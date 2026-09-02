# Hospital Assistant - Visual Guides

## User Query Flow

```
┌────────────────────────────────────────────┐
│          USER STARTS CONVERSATION          │
│                                            │
│    "Hi, I have some questions about..."   │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│         STREAMLIT APP INTERFACE            │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  Chat Input Box                      │  │
│  │  [User types message and presses]    │  │
│  │              SUBMIT                  │  │
│  └──────────────────────────────────────┘  │
└───────────────┬────────────────────────────┘
                │
                ▼
┌────────────────────────────────────────────┐
│    AGENT RECEIVES MESSAGE (agent.py)       │
│                                            │
│  1. Parse user intent                      │
│  2. Review conversation history            │
│  3. Determine message type                 │
└───────────────┬────────────────────────────┘
                │
                ▼
      ┌─────────────────────────┐
      │  QUESTION TYPE?         │
      └────┬────────────┬───────┘
           │            │
      HOSPITAL?      APPOINTMENT?
           │            │
           ▼            ▼
    ┌────────────┐ ┌──────────────────┐
    │ SEARCH     │ │ BOOKING          │
    │ HOSPITAL   │ │ FUNCTIONS        │
    │ INFO       │ │                  │
    │ TOOL       │ │ - book_appt      │
    └─────┬──────┘ │ - cancel_appt    │
          │        │ - wait_time      │
          │        │ - optimal_slots  │
          │        └────────┬─────────┘
          │                 │
          └────────┬────────┘
                   ▼
         ┌──────────────────────┐
         │ TOOL EXECUTES        │
         │                      │
         │ - Gets data          │
         │ - Processes info     │
         │ - Formats response   │
         └──────┬───────────────┘
                │
                ▼
       ┌─────────────────────┐
       │  RETURN RESULTS     │
       │                     │
       │ + Source info       │
       │ + Formatted text    │
       │ + Confidence score  │
       └──────┬──────────────┘
              │
              ▼
     ┌────────────────────────────┐
     │  AGENT SYNTHESIZES         │
     │  RESPONSE                  │
     │                            │
     │  Creates natural language  │
     │  response based on:        │
     │  - Retrieved information   │
     │  - Tool results            │
     │  - Conversation context    │
     └──────┬─────────────────────┘
            │
            ▼
   ┌─────────────────────────┐
   │  DISPLAY TO USER        │
   │                         │
   │  Formatted response in  │
   │  chat interface         │
   │                         │
   │  ✓ Professional         │
   │  ✓ Informative          │
   │  ✓ Well-attributed      │
   │  ✓ Helpful              │
   └─────────────────────────┘
```

## Hospital Information Retrieval Process

```
USER QUESTION: "What services do you offer?"
        │
        ▼
   AGENT DETECTS: "This is a hospital info question"
        │
        ▼
   CALLS: search_hospital_information(query)
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼                                         ▼
   HOSPITAL RETRIEVER ACTIVATED
        │
        ▼
   STEP 1: CONVERT TO EMBEDDINGS
   ────────────────────────────
   Query: "What services do you offer?"
                    │
                    ▼ (Sentence-Transformers)
   Vector: [0.23, -0.41, 0.87, ..., 0.12] (384 dimensions)
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼                                         │
   STEP 2: SEARCH VECTOR STORE                    │
   ─────────────────────────────                  │
   FAISS Vector Store contains:                   │
   ├─ Doc chunk 1: [0.24, -0.39, 0.85, ...]      │
   ├─ Doc chunk 2: [0.22, -0.40, 0.86, ...]      │
   ├─ Doc chunk 3: [0.15, -0.50, 0.80, ...]      │
   ├─ Doc chunk 4: [0.10, -0.60, 0.70, ...]      │
   └─ ... (1000s more chunks)                    │
                    │                            │
                    ▼ (Similarity Calculation)   │
   Find closest vectors:                         │
   ├─ Score: 0.95 (Chunk 1)                      │
   ├─ Score: 0.87 (Chunk 2)                      │
   ├─ Score: 0.82 (Chunk 3)                      │
   └─ Score: 0.71 (Chunk 4)                      │
        │                                         │
        ▼                                         │
   STEP 3: RETRIEVE TOP 4 DOCUMENTS               │
   ────────────────────────────────               │
   [Chunk 1 - Score 0.95]                        │
   Source: hospital_docs/services.pdf            │
   Text: "Our hospital offers comprehensive      │
          services including Cardiology,         │
          Orthopedics, General Surgery..."       │
                                                  │
   [Chunk 2 - Score 0.87]                        │
   Source: hospital website                      │
   Text: "We provide emergency care,             │
          diagnostic services, and..."           │
                                                  │
   [Chunk 3 - Score 0.82]                        │
   Source: hospital_docs/departments.pdf         │
   Text: "Our departments include..."            │
                                                  │
   [Chunk 4 - Score 0.71]                        │
   Source: hospital website                      │
   Text: "Service expansion includes..."         │
        │                                         │
        ▼                                         │
   STEP 4: FORMAT WITH SOURCES                    │
   ──────────────────────────                     │
   Formatted Context:                             │
   ┌─────────────────────────────┐               │
   │ Based on hospital documents, │               │
   │ here's the information...    │               │
   │                             │               │
   │ [Source: services.pdf]      │               │
   │ Our hospital offers...      │               │
   │                             │               │
   │ [Source: hospital website]  │               │
   │ We provide emergency...     │               │
   │                             │               │
   │ [Source: departments.pdf]   │               │
   │ Our departments include...  │               │
   │                             │               │
   │ For more info, contact...   │               │
   └─────────────────────────────┘               │
        │                                         │
        └────────────────────────────────────────┘
                         │
                         ▼
        RETURN TO AGENT WITH CONTEXT
                         │
                         ▼
        AGENT GENERATES RESPONSE
                         │
                         ▼
        DISPLAY TO USER:
        ┌─────────────────────────────┐
        │ Our hospital offers a wide  │
        │ range of services:          │
        │                             │
        │ • Cardiology               │
        │ • Orthopedics              │
        │ • General Surgery          │
        │ • Emergency Care           │
        │ • Diagnostic Services      │
        │                             │
        │ For detailed information   │
        │ about specific services,   │
        │ please feel free to ask!   │
        └─────────────────────────────┘
```

## Appointment Booking Flow (Unchanged)

```
USER QUESTION: "I want to book an appointment"
        │
        ▼
   AGENT DETECTS: "This is an appointment question"
        │
        ▼
   CALLS: book_appointment() [or related tool]
        │
        ├─────────────────────────────────────────┐
        │                                         │
        ▼                                         │
   APPOINTMENT TOOL (EXISTING FUNCTIONALITY)
        │
        ├─ Collect patient information
        ├─ Predict waiting time (ML)
        ├─ Find optimal slots
        ├─ Create appointment record
        └─ Send confirmation
```

## Decision Tree: Information vs. Booking

```
        USER MESSAGE RECEIVED
                │
                ▼
    ┌───────────────────────────┐
    │  DOES IT MENTION:         │
    │  - Hospital info?         │
    │  - Services?              │
    │  - Departments?           │
    │  - Contact?               │
    │  - Visiting hours?        │
    │  - Insurance?             │
    │  - Location?              │
    │  - Other hospital facts?  │
    └───────┬────────────┬──────┘
            │            │
           YES           NO
            │            │
            ▼            ▼
    ┌────────────┐  ┌──────────────────┐
    │ HOSPITAL   │  │ IS IT ABOUT:     │
    │ INFO TOOL  │  │ - Appointment?   │
    │            │  │ - Booking?       │
    │ Search     │  │ - Cancellation?  │
    │ documents  │  │ - Wait times?    │
    │            │  │ - Available      │
    │ Return:    │  │   slots?         │
    │ Services,  │  │                  │
    │ Depts,     │  └────┬────────┬────┘
    │ Hours,     │       │        │
    │ Contact    │      YES      NO
    │ Info       │       │        │
    └────┬───────┘       │        │
         │               ▼        ▼
         │        ┌────────────┐ ┌──────────┐
         │        │APPOINTMENT │ │GENERAL   │
         │        │TOOL        │ │ QUESTION │
         │        │            │ │          │
         │        │Get patient │ │Generate  │
         │        │info,       │ │response  │
         │        │book appt,  │ │using     │
         │        │etc         │ │LLM       │
         │        └─────┬──────┘ └────┬─────┘
         │              │             │
         └──────────────┼─────────────┘
                        │
                        ▼
            ┌────────────────────────┐
            │  GENERATE FINAL        │
            │  RESPONSE TO USER      │
            └────────────────────────┘
```

## System Initialization Timeline

```
APPLICATION START
        │
        ▼
   0s: Load Streamlit App
        │
        ▼
   1s: Initialize Configuration
        │
        ├─ Load config.py
        ├─ Load settings.yaml
        ├─ Setup logger
        └─ Initialize LLM connection
        │
        ▼
   2s: Check Session State
        │
        ├─ IF 'initialized' not in session:
        │  └─ Set up session state
        │     │
        │     ▼
        │  3s: Call setup_hospital_knowledge_base()
        │     │
        │     ├─ Scan hospital_docs/ folder
        │     ├─ List found PDF files
        │     │
        │     ▼
        │  5s: Load Documents
        │     │
        │     ├─ Load PDFs with PyPDFLoader
        │     ├─ Extract text from each
        │     ├─ Load website content (if URLs configured)
        │     │
        │     ▼
        │ 20s: Chunk Documents
        │     │
        │     ├─ Split into 1000-char chunks
        │     ├─ Add 200-char overlap
        │     │
        │     ▼
        │ 25s: Create Embeddings
        │     │
        │     ├─ Convert chunks to vectors
        │     ├─ Use sentence-transformers
        │     │ (This is the slow step: ~30-45 sec)
        │     │
        │     ▼
        │ 60s: Build Vector Store
        │     │
        │     ├─ Create FAISS index
        │     ├─ Save to hospital_vector_store/
        │     │
        │     ▼
        │ 65s: Done! System Ready
        │
        ├─ ELSE if 'initialized' in session:
        │  └─ Load existing vector store
        │     (Fast: < 100ms)
        │
        ▼
   65-70s: Display UI
        │
        ▼
   Application Ready for Use!
```

## Data Flow Diagram: Complete Request

```
┌──────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│                   (Streamlit Chat)                       │
└─────────────────────┬──────────────────────────────────┘
                      │ User types message & submits
                      ▼
        ┌──────────────────────────────────┐
        │     Message goes to Agent        │
        │  (LangGraph State Machine)       │
        └──────────────┬───────────────────┘
                       │
                       ▼ Agent analyzes message
        ┌──────────────────────────────────┐
        │  Determine Tool to Use           │
        │  ├─ Hospital Info Tool?          │
        │  ├─ Appointment Tool?            │
        │  └─ Direct LLM Response?         │
        └──────┬──────────────────┬────────┘
               │                  │
        Hospital Info?      Appointment?
               │                  │
               ▼                  ▼
    ┌─────────────────┐  ┌─────────────────┐
    │Hospital Retriever  │Appointment Tools  │
    │   (New Code)       │  (Existing)      │
    └─────┬─────────────┘  └────────┬────────┘
          │                         │
          ├─ Query to Embeddings    ├─ Collect Patient Info
          ├─ Search Vector Store    ├─ Check ML Models
          ├─ Get Top 4 Docs         ├─ Predict Wait Times
          ├─ Format with Sources    ├─ Find Optimal Slots
          └─ Return Context         └─ Create Appointment
                │                         │
                └────────────┬────────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │   Agent Synthesizes    │
                │   Response Using:      │
                │  ├─ Tool Results       │
                │  ├─ Conversation      │
                │  │  History            │
                │  └─ System Prompt      │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │   Generate Response    │
                │   (Groq LLM)          │
                │  llama-3.3-70b        │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │   Format Response      │
                │  ├─ Add markdown       │
                │  ├─ Structure text     │
                │  └─ Add emojis         │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │   Add to Chat History  │
                │   (Conversation list)  │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │   Display in UI        │
                │                        │
                │  Response appears      │
                │  in chat box           │
                │  User can see it       │
                └────────────────────────┘
```

## Component Interaction Map

```
                        ┌─────────────┐
                        │  Streamlit  │
                        │    UI       │
                        └──────┬──────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
            ┌──────────────────┐  ┌──────────────┐
            │   Hospital       │  │ Appointments │
            │   Setup          │  │ Database     │
            │ (hospital_setup) │  │ (existing)   │
            └──────┬───────────┘  └──────────────┘
                   │                     ▲
                   ▼                     │
        ┌────────────────────┐           │
        │  Hospital          │           │
        │  Retriever         │           │
        │(hospital_retriever)│           │
        └────────┬───────────┘           │
                 │                       │
                 ├─ PDF Loader           │
                 ├─ Web Scraper          │
                 ├─ Text Chunker         │
                 ├─ Embeddings           │
                 └─ FAISS Vector Store   │
                                        │
                 ┌──────────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  Hospital Tools    │
        │ (hospital_tools)   │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  LangChain Agent   │
        │   (agent.py)       │
        │                    │
        │  ├─ Tool Router    │
        │  ├─ LLM Bridge     │
        │  ├─ State Manager  │
        │  └─ Response Gen   │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  Groq LLM          │
        │ llama-3.3-70b      │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │  Back to Streamlit │
        │  Display Response  │
        └────────────────────┘
```

These visual guides help understand how the system works and how information flows through it!
