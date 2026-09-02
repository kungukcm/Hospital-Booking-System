from langchain_community.document_loaders import PyPDFLoader

try:
    loader = PyPDFLoader('hospital_docs/KUTTRH-Service-Charter.pdf')
    docs = loader.load()
    print(f'✅ SUCCESS: Loaded {len(docs)} pages from Service Charter')
    print(f'First 200 characters: {docs[0].page_content[:200]}...')
except Exception as e:
    print(f'❌ ERROR: {str(e)}')
