from rag_agent.app.ingestion.create_embeddings import ChunkVectorizer

vectorizer = ChunkVectorizer(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    chunk_dir="C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\\data\\processed\\chunks",
    batch_size=64
)

vectorizer.run_pipeline(output_file="C:\\Users\\Michael\\PycharmProjects\\PersonalRAG\\rag_agent\\data\\processed\\embeddings\\embeddings.json")

print(vectorizer.embeddings[0].shape)
print(vectorizer.metadata[0])