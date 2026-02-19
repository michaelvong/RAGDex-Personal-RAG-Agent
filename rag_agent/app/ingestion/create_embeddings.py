import os
import json
import glob
import hashlib
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer


class ChunkVectorizer:
    def __init__(self, 
                 model_name="sentence-transformers/all-MiniLM-L6-v2", 
                 chunk_dir="C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\\data\\processed",
                 batch_size=64,
                 device=None):
        self.chunk_dir = chunk_dir
        self.batch_size = batch_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.chunks = []
        self.metadata = []
        self.ids = []
        self.embeddings = []

    # -------------------------------
    # Load all JSON chunk files
    # -------------------------------
    def load_chunks(self):
        print(self.chunk_dir)
        json_files = glob.glob(os.path.join(self.chunk_dir, "*.json"))
        print(f"Found {len(json_files)} JSON files:")
        for f in json_files:
            print(f)
        for file in json_files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    text = item.get("text", "").strip()
                    if not text:
                        continue

                    chunk_id = item.get(
                        "id", hashlib.md5(text.encode("utf-8")).hexdigest()
                    )
                    meta = {
                        "source": item.get("source", "unknown"),
                        "chunk_index": item.get("chunk_index", -1)
                    }

                    self.chunks.append(text)
                    self.metadata.append(meta)
                    self.ids.append(chunk_id)
        print(f"Loaded {len(self.chunks)} chunks")

    # -------------------------------
    # Deduplicate chunks by ID
    # -------------------------------
    def deduplicate_chunks(self):
        unique = {}
        for text, meta, cid in zip(self.chunks, self.metadata, self.ids):
            if cid not in unique:
                unique[cid] = (text, meta)
        self.ids = list(unique.keys())
        self.chunks = [unique[cid][0] for cid in self.ids]
        self.metadata = [unique[cid][1] for cid in self.ids]
        print(f"After deduplication: {len(self.chunks)} chunks")

    # -------------------------------
    # Batch embedding of chunks
    # -------------------------------
    def embed_chunks(self, normalize=True):
        self.embeddings = []

        for i in tqdm(range(0, len(self.chunks), self.batch_size)):
            batch_texts = self.chunks[i:i + self.batch_size]
            batch_embeddings = self.model.encode(
                batch_texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=normalize
            )
            self.embeddings.extend(batch_embeddings)
        print(f"Embedded {len(self.embeddings)} chunks")

    # -------------------------------
    # Save embeddings + metadata to JSON
    # -------------------------------
    def save_to_json(self, output_file="embeddings.json"):
        output_data = []
        for cid, text, meta, emb in zip(self.ids, self.chunks, self.metadata, self.embeddings):
            output_data.append({
                "id": cid,
                "text": text,
                "metadata": meta,
                "embedding": emb.tolist()
            })

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f)
        print(f"Saved {len(output_data)} embeddings to {output_file}")

    # -------------------------------
    # Full pipeline: load → deduplicate → embed → save
    # -------------------------------
    def run_pipeline(self, output_file="embeddings.json"):
        self.load_chunks()
        self.deduplicate_chunks()
        self.embed_chunks()
        self.save_to_json(output_file)
