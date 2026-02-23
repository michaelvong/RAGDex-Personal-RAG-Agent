import os
import json
import glob
import hashlib
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer


class ChunkVectorizer:
    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        chunk_dir=r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\data\processed\chunks",
        output_dir=r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\data\processed\embeddings",
        batch_size=64,
        device=None,
    ):
        self.chunk_dir = chunk_dir
        self.output_dir = output_dir
        self.batch_size = batch_size
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)

    # -------------------------------
    # Process ONE domain file
    # -------------------------------
    def process_file(self, chunk_path):
        filename = os.path.basename(chunk_path)
        domain_name = filename.replace("_chunks.json", "")
        output_path = os.path.join(self.output_dir, f"{domain_name}_embeddings.json")

        with open(chunk_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks = []
        metadata = []
        ids = []

        for item in data:
            text = item.get("text", "").strip()
            if not text:
                continue

            chunk_id = item.get(
                "id", hashlib.md5(text.encode("utf-8")).hexdigest()
            )

            meta = {
                "source": item.get("source", "unknown"),
                "chunk_index": item.get("chunk_index", -1),
                "domain": domain_name,  # 🔥 domain tag for filtering later
            }

            chunks.append(text)
            metadata.append(meta)
            ids.append(chunk_id)

        print(f"[{domain_name}] Loaded {len(chunks)} chunks")

        # Deduplicate
        unique = {}
        for text, meta, cid in zip(chunks, metadata, ids):
            if cid not in unique:
                unique[cid] = (text, meta)

        ids = list(unique.keys())
        chunks = [unique[cid][0] for cid in ids]
        metadata = [unique[cid][1] for cid in ids]

        print(f"[{domain_name}] After dedup: {len(chunks)} chunks")

        # Embed
        embeddings = []

        for i in tqdm(range(0, len(chunks), self.batch_size), desc=f"Embedding {domain_name}"):
            batch_texts = chunks[i:i + self.batch_size]
            batch_embeddings = self.model.encode(
                batch_texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
            embeddings.extend(batch_embeddings)

        # Save
        os.makedirs(self.output_dir, exist_ok=True)

        output_data = []
        for cid, text, meta, emb in zip(ids, chunks, metadata, embeddings):
            output_data.append({
                "id": cid,
                "text": text,
                "metadata": meta,
                "embedding": emb.tolist(),
            })

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f)

        print(f"[{domain_name}] Saved {len(output_data)} embeddings → {output_path}")

    # -------------------------------
    # Process ALL domains
    # -------------------------------
    def run_pipeline(self):
        chunk_files = glob.glob(os.path.join(self.chunk_dir, "*_chunks.json"))

        if not chunk_files:
            raise ValueError(f"No chunk files found in {self.chunk_dir}")

        print(f"Found {len(chunk_files)} domain files")

        for chunk_path in chunk_files:
            self.process_file(chunk_path)