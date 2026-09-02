from langchain_community.document_loaders import PyPDFLoader

# Load the Service Charter to see what payment info is in it
loader = PyPDFLoader('hospital_docs/KUTTRH-Service-Charter.pdf')
docs = loader.load()

print(f"KUTTRH Service Charter - {len(docs)} pages")
print("\n" + "="*80)

for i, doc in enumerate(docs):
    content = doc.page_content.lower()
    # Search for payment-related keywords
    if any(keyword in content for keyword in ['payment', 'pay', 'tariff', 'charge', 'fee', 'bill', 'cost']):
        print(f"\nPage {i+1} contains payment-related content:")
        print("-" * 80)
        # Find and print the relevant section
        lines = doc.page_content.split('\n')
        for j, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in ['payment', 'pay', 'tariff', 'charge', 'fee', 'bill']):
                # Print context around the match
                start = max(0, j-2)
                end = min(len(lines), j+3)
                print('\n'.join(lines[start:end]))
                print()
                break
