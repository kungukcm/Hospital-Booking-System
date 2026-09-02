import os
os.environ['PYTHONHASHSEED'] = '0'

from hospital_setup import setup_hospital_knowledge_base

print("Starting hospital knowledge base setup...")
result = setup_hospital_knowledge_base()
print(f"Setup result: {result}")

# Check if vector store was created
import os
if os.path.exists("hospital_vector_store"):
    print("✅ Vector store created successfully!")
    files = os.listdir("hospital_vector_store")
    print(f"Files in vector store: {files}")
else:
    print("❌ Vector store not created!")
