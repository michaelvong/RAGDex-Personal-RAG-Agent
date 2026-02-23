import json
import os
import glob
import chromadb
from chromadb.config import Settings

class ChromaIngestor:
    def __init__(self, chroma_dir, collection_name, embeddings_dir):
        self.chroma_dir = os.path.abspath(chroma_dir)
        self.collection_name = collection_name
        self.embeddings_dir = os.path.abspath(embeddings_dir)

        # Make sure the folder exists
        os.makedirs(self.chroma_dir, exist_ok=True)

        # Initialize Chroma (auto-persistent in latest versions)
        self.client = chromadb.PersistentClient(path=self.chroma_dir, settings=Settings())
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

        self.ids = []
        self.docs = []
        self.metadatas = []
        self.vectors = []

    def load_all_json(self):
        embedding_files = glob.glob(os.path.join(self.embeddings_dir, "*_embeddings.json"))
        if not embedding_files:
            raise ValueError(f"No embedding JSON files found in {self.embeddings_dir}")
        print(f"Found {len(embedding_files)} embedding files")

        for emb_path in embedding_files:
            print(f"Loading {emb_path}")
            with open(emb_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                self.ids.append(item["id"])
                self.docs.append(item["text"])
                self.metadatas.append(item.get("metadata", {}))
                self.vectors.append(item["embedding"])
        print(f"Loaded {len(self.ids)} total embeddings")

    def _filter_existing_ids(self):
        if not self.ids:
            return

        print("Checking for existing IDs in Chroma...")

        existing = set()
        batch_size = 1000

        for i in range(0, len(self.ids), batch_size):
            batch_ids = self.ids[i:i + batch_size]
            result = self.collection.get(ids=batch_ids)
            if result and "ids" in result:
                existing.update(result["ids"])

        if not existing:
            print("No existing IDs found in Chroma.")
            return

        print(f"Skipping {len(existing)} existing embeddings")

        new_data = [
            (i, d, m, v)
            for i, d, m, v in zip(self.ids, self.docs, self.metadatas, self.vectors)
            if i not in existing
        ]

        if not new_data:
            self.ids, self.docs, self.metadatas, self.vectors = [], [], [], []
            return

        self.ids, self.docs, self.metadatas, self.vectors = map(list, zip(*new_data))

    def ingest(self, batch_size=500):
        if not self.ids:
            print("No data to ingest.")
            return

        # Remove duplicates already in Chroma
        self._filter_existing_ids()

        if not self.ids:
            print("No new embeddings to add.")
            return

        print(f"Adding {len(self.ids)} new embeddings to Chroma...")

        for i in range(0, len(self.ids), batch_size):
            self.collection.add(
                ids=self.ids[i:i + batch_size],
                embeddings=self.vectors[i:i + batch_size],
                documents=self.docs[i:i + batch_size],
                metadatas=self.metadatas[i:i + batch_size],
            )
        print(f"Stored {len(self.ids)} embeddings in Chroma (auto-persisted).")
        print(f"Chroma DB folder: {self.chroma_dir}")