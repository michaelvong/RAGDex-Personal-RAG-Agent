import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
import nltk

# ---------- Safe NLTK punkt download ---------- #
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

from nltk.tokenize import sent_tokenize

# ---------- Safe sentence tokenizer fallback ---------- #
def safe_sent_tokenize(text: str) -> List[str]:
    try:
        return sent_tokenize(text)
    except LookupError:
        # fallback if punkt fails
        return [s.strip() for s in text.split(".") if s.strip()]

# ---------- File hash function ---------- #
def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 hash of a file for change detection"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# ---------- Document Loader ---------- #
class DocumentLoader:
    def __init__(
        self,
        raw_dir: str,
        processed_dir: str,
        chunk_size: int = 5,
        log_file: str = None,
        use_hashing: bool = True  # FEATURE FLAG: enable/disable skipping processed files
    ):
        """
        :param raw_dir: path to raw documents
        :param processed_dir: path to save processed chunks
        :param chunk_size: sentences per chunk
        :param log_file: path to JSON file tracking processed files and hashes
        :param use_hashing: if False, all files are reprocessed regardless of log
        """
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.chunk_size = chunk_size
        self.use_hashing = use_hashing

        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = Path(log_file) if log_file else self.processed_dir / "processed_files.json"

        # Load existing processing log
        if self.log_file.exists():
            with open(self.log_file, "r", encoding="utf-8") as f:
                self.process_log = json.load(f)
        else:
            self.process_log = {}

    # ---------- PDF Extraction ---------- #
    def pdf_to_text(self, file_path: Path) -> str:
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

    def pdf_to_text_ocr(self, file_path: Path) -> str:
        text = ""
        try:
            pages = convert_from_path(file_path)
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        except Exception as e:
            print(f"OCR failed for {file_path}: {e}")
        return text

    # ---------- Text Loading ---------- #
    def load_text_file(self, file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def normalize_text(self, text: str) -> str:
        return "\n".join([line.strip() for line in text.splitlines() if line.strip()])

    def chunk_text(self, text: str, chunk_size_tokens: int = 400, overlap_tokens: int = 80) -> List[str]:
        """
        Chunk text into token-based chunks with optional overlap.
        Keeps chunks semantically coherent by joining sentences.

        :param text: input text
        :param chunk_size_tokens: target tokens per chunk
        :param overlap_tokens: number of tokens to overlap between consecutive chunks
        """
        # Step 1: tokenize into sentences
        sentences = safe_sent_tokenize(text)

        # Step 2: build token-based chunks
        chunks = []
        current_chunk = []
        current_len = 0  # token count in current chunk

        for sentence in sentences:
            sentence_tokens = sentence.split()  # crude token count
            sentence_len = len(sentence_tokens)

            # if adding this sentence exceeds chunk size, finalize current chunk
            if current_len + sentence_len > chunk_size_tokens and current_chunk:
                chunks.append(" ".join(current_chunk))

                # start new chunk with overlap
                if overlap_tokens > 0:
                    # keep last few tokens as overlap
                    overlap_tokens_list = " ".join(current_chunk).split()[-overlap_tokens:]
                    current_chunk = [" ".join(overlap_tokens_list)]
                    current_len = len(overlap_tokens_list)
                else:
                    current_chunk = []
                    current_len = 0

            # add sentence to current chunk
            current_chunk.append(sentence)
            current_len += sentence_len

        # add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    # ---------- Chunk ID generator ---------- #
    def generate_chunk_id(self, domain: str, chunk_text: str, chunk_idx: int) -> str:
        """
        Generate a globally unique, human-readable chunk ID.
        Does NOT include the file name.
        """
        # Use a hash of the chunk text (first 8 chars for brevity)
        text_hash = hashlib.sha1(chunk_text.encode("utf-8")).hexdigest()[:8]
        return f"{domain}_{text_hash}_chunk{chunk_idx}"

    # ---------- File Processing ---------- #
    def process_document(self, file_path: Path, domain: str) -> List[Dict]:
        file_hash = compute_file_hash(file_path)
        file_key = str(file_path)

        # SKIP if hashing is enabled and file already processed
        if self.use_hashing:
            if file_key in self.process_log and self.process_log[file_key] == file_hash:
                print(f"Skipping already processed file: {file_path.name}")
                return []

        # Extract text
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            text = self.pdf_to_text(file_path)
            if not text.strip():
                text = self.pdf_to_text_ocr(file_path)
        elif ext in [".md", ".txt"]:
            text = self.load_text_file(file_path)
        else:
            print(f"Unsupported file type: {file_path}")
            return []

        text = self.normalize_text(text)
        chunks = self.chunk_text(text)

        # Create processed chunks with metadata
        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            chunk_id = self.generate_chunk_id(domain, chunk, idx)
            processed_chunks.append(
                {
                    "text": chunk,
                    "source": str(file_path.name),
                    "domain": domain,
                    "chunk_id": chunk_id,
                }
            )

        # Update processing log only if hashing enabled
        if self.use_hashing:
            self.process_log[file_key] = file_hash

        return processed_chunks

    # ---------- Batch Processing ---------- #
    def process_all(self):
        """
        Process all raw files in self.raw_dir.
        Ensures each domain JSON is a valid array [].
        Updates chunks incrementally:
          - skips unchanged files if use_hashing=True
          - removes old chunks for updated files
          - appends new chunks
        """
        if not self.raw_dir.exists():
            print(f"Raw directory {self.raw_dir} does not exist.")
            return

        for domain_dir in self.raw_dir.iterdir():
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            output_file = self.processed_dir / f"{domain}_chunks.json"

            # Load existing chunks as a list; if file missing or invalid, start with empty list
            all_chunks = []
            if output_file.exists():
                try:
                    all_chunks = json.load(open(output_file, "r", encoding="utf-8"))
                    if not isinstance(all_chunks, list):
                        print(f"Warning: {output_file} not a list; resetting to empty list.")
                        all_chunks = []
                except json.JSONDecodeError:
                    print(f"Warning: {output_file} is invalid JSON; resetting to empty list.")
                    all_chunks = []

            # Build a map: source file -> list of chunk indices in all_chunks
            source_index_map = {}
            for idx, chunk in enumerate(all_chunks):
                source_file = chunk.get("source")
                if source_file not in source_index_map:
                    source_index_map[source_file] = []
                source_index_map[source_file].append(idx)

            # Process each file in the domain
            for file_path in tqdm(list(domain_dir.iterdir()), desc=f"Processing {domain}"):
                new_chunks = self.process_document(file_path, domain)
                if not new_chunks:
                    continue  # skipped or unsupported file

                # Remove old chunks from this file if they exist
                old_indices = source_index_map.get(file_path.name, [])
                for i in sorted(old_indices, reverse=True):
                    del all_chunks[i]

                # Append new chunks
                all_chunks.extend(new_chunks)

            # Save updated chunks list as valid JSON array
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_chunks, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(all_chunks)} chunks to {output_file}")

        # Save updated processing log
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.process_log, f, ensure_ascii=False, indent=2)
        print(f"Updated processing log: {self.log_file}")
