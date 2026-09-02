# Hospital Document Integration - Quick Start

## 5-Minute Setup Guide

### What's New
Your AI hospital booking assistant now has the ability to answer questions about hospital services, departments, contact info, and more by retrieving information from hospital PDFs and websites.

### Quick Setup Steps

#### 1. **Create Documents Folder**
```bash
# In your project directory, create the hospital_docs folder
mkdir hospital_docs
```

#### 2. **Add Hospital PDFs**
Place your hospital documentation PDFs in the `hospital_docs/` folder. Examples:
- `hospital_services.pdf` - Services offered
- `departments.pdf` - Department information
- `contact_info.pdf` - Phone, email, address
- `visiting_hours.pdf` - When can visitors come?
- `insurance.pdf` - Insurance and payment information

#### 3. **Install New Dependencies**
```bash
pip install -r requirements.txt
```

#### 4. **Run the App**
```bash
streamlit run app.py
```

That's it! The knowledge base will be built automatically on first run.

### How It Works in the App

Users can now ask questions like:
- "What are your visiting hours?"
- "What departments do you have?"
- "How do I contact the hospital?"
- "Do you accept my insurance?"
- "What services do you provide?"

The assistant will search hospital documents and provide relevant answers.

### Testing Without PDFs

If you don't have PDFs yet, the system will try to retrieve information from the hospital website (if configured). The app will still work for appointment booking.

### Folder Structure
```
your-project/
├── hospital_docs/          ← Add PDFs here
│   ├── services.pdf
│   ├── departments.pdf
│   └── contact.pdf
├── hospital_vector_store/  ← Auto-created on first run
├── app.py
├── agent.py
├── hospital_retriever.py   ← New
├── hospital_tools.py       ← New
├── hospital_setup.py       ← New
└── requirements.txt        ← Updated
```

### New Files Added to Your Project

1. **hospital_retriever.py** - Core retrieval system using FAISS
2. **hospital_tools.py** - LangChain tool for the agent
3. **hospital_setup.py** - Setup and initialization
4. **HOSPITAL_DOCUMENT_INTEGRATION.md** - Full documentation

### Configuration (Optional)

Edit `hospital_setup.py` to customize:

```python
DEFAULT_HOSPITAL_CONFIG = {
    "hospital_name": "Your Hospital Name",
    "website_urls": [
        "https://yourhospital.com",
        "https://yourhospital.com/departments"
    ],
    "pdf_directory": "hospital_docs"  # Change if needed
}
```

### Troubleshooting

**Q: Knowledge base not loading?**
- Ensure `hospital_docs/` folder exists
- Place at least one PDF in the folder
- Check terminal for error messages

**Q: Slow on first run?**
- Normal - embeddings are being created
- Subsequent runs will be faster (cached)

**Q: Not finding hospital information?**
- Ensure PDFs have good text (not scanned images)
- Add more PDFs covering the topic
- Ask specific questions about content

### Next Steps

1. Add hospital PDFs to `hospital_docs/`
2. Run `streamlit run app.py`
3. Test by asking hospital information questions
4. Appointment booking still works as before
5. See HOSPITAL_DOCUMENT_INTEGRATION.md for advanced options

### Key Features

✅ **Semantic Search** - Finds relevant information based on meaning, not just keywords
✅ **Multi-Source** - Combines PDFs and website content
✅ **Fast Lookups** - Vector store is cached for speed
✅ **Source Attribution** - Shows where information came from
✅ **Seamless Integration** - Works alongside existing appointment booking

### Support

For detailed information, see [HOSPITAL_DOCUMENT_INTEGRATION.md](HOSPITAL_DOCUMENT_INTEGRATION.md)

---

**Ready to integrate hospital documents? Add your PDFs to `hospital_docs/` and restart the app!**
