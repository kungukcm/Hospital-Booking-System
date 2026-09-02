"""
Example Usage and Testing for Hospital Document Retrieval
Run this file to test the hospital retrieval system
"""

import os
from hospital_setup import setup_hospital_knowledge_base, DEFAULT_HOSPITAL_CONFIG
from hospital_tools import search_hospital_information, initialize_hospital_knowledge_base
from logger import setup_logger

logger = setup_logger(__name__)


def example_basic_usage():
    """Example 1: Basic setup and query"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Setup and Query")
    print("="*60)
    
    # Setup knowledge base
    print("\n1. Setting up hospital knowledge base...")
    success = setup_hospital_knowledge_base(
        pdf_directory="hospital_docs",
        website_urls=[
            "https://www.kutrrh.go.ke"
        ]
    )
    
    if success:
        print("✓ Knowledge base initialized successfully")
    else:
        print("⚠ Knowledge base setup had issues, but continuing...")
    
    # Test query
    print("\n2. Testing hospital information search...")
    query = "What departments and services do you offer?"
    print(f"Query: {query}")
    
    result = search_hospital_information(query)
    print(f"\nResponse:\n{result}")


def example_multiple_queries():
    """Example 2: Multiple different queries"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Queries")
    print("="*60)
    
    # Sample queries
    queries = [
        "What are the hospital visiting hours?",
        "How do I contact the hospital?",
        "What insurance plans do you accept?",
        "Do you have an emergency department?",
        "What are the hospital services?",
        "Where is the hospital located?",
    ]
    
    print("\nRunning test queries...\n")
    
    for i, query in enumerate(queries, 1):
        print(f"{i}. Query: {query}")
        result = search_hospital_information(query)
        print(f"   Response: {result[:200]}...")  # First 200 chars
        print()


def example_custom_pdf_directory():
    """Example 3: Custom PDF directory"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom PDF Directory")
    print("="*60)
    
    # Use custom PDF directory
    custom_pdf_dir = "my_hospital_docs"
    
    # Create directory if it doesn't exist
    if not os.path.exists(custom_pdf_dir):
        os.makedirs(custom_pdf_dir)
        print(f"✓ Created directory: {custom_pdf_dir}")
    
    # Setup with custom directory
    print(f"\nSetting up with custom directory: {custom_pdf_dir}")
    success = setup_hospital_knowledge_base(
        pdf_directory=custom_pdf_dir
    )
    
    if success:
        print("✓ Custom directory setup successful")
    else:
        print("⚠ No PDFs found in custom directory")


def example_hospital_config():
    """Example 4: Using hospital configuration"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Hospital Configuration")
    print("="*60)
    
    print("\nDefault Hospital Configuration:")
    print(f"  Hospital Name: {DEFAULT_HOSPITAL_CONFIG['hospital_name']}")
    print(f"  Hospital Code: {DEFAULT_HOSPITAL_CONFIG['hospital_code']}")
    print(f"  PDF Directory: {DEFAULT_HOSPITAL_CONFIG['pdf_directory']}")
    print(f"  Website URLs: {len(DEFAULT_HOSPITAL_CONFIG['website_urls'])} URLs configured")
    
    for url in DEFAULT_HOSPITAL_CONFIG['website_urls']:
        print(f"    - {url}")


def example_error_handling():
    """Example 5: Error handling"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Error Handling")
    print("="*60)
    
    print("\nTesting with non-existent PDF directory...")
    
    # This should handle gracefully
    success = setup_hospital_knowledge_base(
        pdf_directory="non_existent_directory",
        website_urls=[]
    )
    
    if success:
        print("✓ Setup successful")
    else:
        print("✓ Gracefully handled missing directory")
    
    # Query with uninitialized knowledge base
    print("\nQuerying with uninitialized knowledge base...")
    result = search_hospital_information("What services do you offer?")
    print(f"Response: {result}")


def example_integration_with_agent():
    """Example 6: How this integrates with the agent"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Agent Integration")
    print("="*60)
    
    print("""
When a user asks a hospital information question, the agent:

1. Detects the query is about hospital information (not appointment booking)
2. Calls the search_hospital_information() tool
3. Tool retrieves relevant documents using semantic search
4. Tool returns formatted context with sources
5. Agent provides response based on retrieved information

Example conversation flow:

User: "What departments do you have?"
Agent: [Calls search_hospital_information("What departments do you have?")]
Agent Response: "Based on our hospital documents, we have the following departments:
[Lists departments from retrieved documents]"

User: "Can I book an appointment in cardiology?"
Agent: [Switches to appointment booking tools]
Agent Response: "Of course! To book a cardiology appointment, I'll need..."
""")


def example_setup_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("SETUP INSTRUCTIONS")
    print("="*60)
    
    print("""
1. CREATE HOSPITAL_DOCS FOLDER:
   mkdir hospital_docs

2. ADD YOUR PDFs:
   Place hospital PDF documents in hospital_docs/
   Examples: services.pdf, departments.pdf, contact.pdf

3. INSTALL DEPENDENCIES:
   pip install -r requirements.txt

4. RUN THE APP:
   streamlit run app.py

5. TEST:
   Ask the assistant: "What services do you provide?"
   Assistant will search hospital documents and respond.

For more details, see:
- HOSPITAL_DOCUMENT_INTEGRATION.md - Full documentation
- HOSPITAL_DOCS_QUICKSTART.md - Quick start guide
""")


def run_all_examples():
    """Run all examples"""
    print("\n" + "="*60)
    print("HOSPITAL DOCUMENT RETRIEVAL - EXAMPLES")
    print("="*60)
    
    # Show setup instructions first
    example_setup_instructions()
    
    # Run examples
    try:
        example_basic_usage()
    except Exception as e:
        print(f"Note: Example 1 requires PDFs in hospital_docs/ folder")
        logger.warning(f"Example 1 failed: {e}")
    
    example_hospital_config()
    
    try:
        example_multiple_queries()
    except Exception as e:
        logger.warning(f"Example 2 failed: {e}")
    
    try:
        example_custom_pdf_directory()
    except Exception as e:
        logger.warning(f"Example 3 failed: {e}")
    
    example_error_handling()
    example_integration_with_agent()
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETE")
    print("="*60)
    print("""
Next steps:
1. Add hospital PDFs to hospital_docs/ folder
2. Run: streamlit run app.py
3. Test with questions about hospital services

For full documentation, see HOSPITAL_DOCUMENT_INTEGRATION.md
""")


if __name__ == "__main__":
    run_all_examples()
