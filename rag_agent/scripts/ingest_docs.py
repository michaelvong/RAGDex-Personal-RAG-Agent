from rag_agent.app.ingestion.document_loader import DocumentLoader

# Initialize loader
loader = DocumentLoader(
    raw_dir="C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\data\\raw",
    processed_dir="C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\data\\processed",
    chunk_size=5,
    log_file="data/processed/processed_files.json",
    use_hashing=False
)

# Run full ingestion
loader.process_all()
