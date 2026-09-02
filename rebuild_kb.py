import os, shutil
from hospital_setup import setup_hospital_knowledge_base

print("Rebuilding hospital knowledge base...", flush=True)
# Remove vector store if present
vp = "hospital_vector_store"
if os.path.exists(vp):
    shutil.rmtree(vp)
    print("Deleted existing vector store", flush=True)

ok = setup_hospital_knowledge_base()
print(f"Setup result: {ok}", flush=True)

# Show contents of the new vector store
if os.path.exists(vp):
    files = os.listdir(vp)
    print("Vector store files:", files, flush=True)
else:
    print("Vector store not found after rebuild!", flush=True)
