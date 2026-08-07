# one-off script — list_collections.py
from backend.rag.vectorstore import VectorStore

vs = VectorStore()
chroma_instance = vs._VectorStore__get_collection("placeholder")  # name-mangled since it's "private" via __
# or simpler: just access the underlying persistent client directly

import chromadb
from backend.config.settings import settings

client = chromadb.PersistentClient(path=str(settings.CHROMA_DIRECTORY))
for collection in client.list_collections():
    print(collection.name, "-", collection.count(), "chunks")