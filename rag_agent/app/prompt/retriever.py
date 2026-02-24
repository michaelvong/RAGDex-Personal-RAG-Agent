# rag_retriever.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGRetriever:
    """
    Handles embedding queries, retrieving top-k relevant chunks from Chroma DB,
    and preparing context for LLM.
    """

    def __init__(self, chroma_dir: str = r"C:\Users\Michael\PycharmProjects\PersonalRAG\rag_agent\chroma_db", collection_name: str = "rag_chunks",
                 embedding_model_name: str = "all-MiniLM-L6-v2"):
        # Initialize Chroma client and collection
        self.client = chromadb.PersistentClient(path=chroma_dir)
        self.collection = self.client.get_collection(collection_name)

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def embed_query(self, query: str):
        """
        Embed a single query into a vector.
        """
        return self.embedding_model.encode([query], convert_to_numpy=True)

    def retrieve(self, query: str, top_k: int = 5, metadata_filter: dict = None) -> str:
        """
        Retrieve top_k document chunks from Chroma DB based on query similarity.
        Optionally filter by metadata.
        """
        query_emb = self.embed_query(query)

        if metadata_filter:
            results = self.collection.query(
                query_embeddings=query_emb,
                n_results=top_k,
                where=metadata_filter
            )
        else:
            results = self.collection.query(
                query_embeddings=query_emb,
                n_results=top_k
            )

        retrieved_docs = results['documents'][0]
        context = "\n".join(retrieved_docs)
        return context

if __name__ == "__main__":
    retriever = RAGRetriever(collection_name="rag_chunks")

    query = "What AWS services did I use in my Serverless Project Board?"
    context = retriever.retrieve(query, top_k=3)
    print("Retrieved Context:\n", context)