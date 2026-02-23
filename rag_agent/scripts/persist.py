from rag_agent.app.ingestion.store_embeddings import ChromaIngestor
import chromadb
from chromadb.config import Settings
import os
ingestor = ChromaIngestor(
    chroma_dir=r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\chroma_db",
    collection_name="rag_chunks",
    embeddings_dir=r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\data\processed\embeddings",
)

ingestor.load_all_json()
ingestor.ingest()

#client = chromadb.PersistentClient(path=r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\chroma_db")
#collection = client.get_collection("rag_chunks")
#print("Vector count:", collection.count())
#results = collection.get(limit=1, include=['embeddings'])
#print(results)