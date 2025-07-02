import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.utils.embedding import ingest_docs


roles = ["hr"]

for role in roles:
    print(f"\n Ingesting data for role: {role}")
    try:
        persist_dir = f"vectorstore/{role}"
        ingest_docs(role, persist_dir)
        print(f"Done with {role}")
    except Exception as e:
        print(f"Error ingesting {role}: {e}")
