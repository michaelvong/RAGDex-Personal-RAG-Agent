from rag_agent.app.ingestion.document_loader import DocumentLoader

BASE_DIR = "C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\\"

# Initialize loader
loader = DocumentLoader(
    raw_dir= BASE_DIR + "data\\raw",
    processed_dir= BASE_DIR + "data\\processed\\chunks",
    chunk_size=5,
    log_file= BASE_DIR + "data\\processed\\logs\\processed_files.json",
    use_hashing=False
)

# Run full ingestion
loader.process_all()
