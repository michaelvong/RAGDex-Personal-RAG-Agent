# rag_retriever.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

L2_threshold = 1.15

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

    def retrieve_v2(self, query: str, top_k: int=5) -> str:
        query_emb = self.embed_query(query)
        results = self.collection.query(
            query_embeddings=query_emb,
            n_results=top_k
        )
        filtered_docs = []
        for i in range(0, len(results['documents'][0])):
            L2_distance = float(results['distances'][0][i]) #L2 distance is given by Chroma DB after doing similarity search
            if L2_distance < L2_threshold:
                filtered_docs.append(results['documents'][0][i])

        #case if no context matches, return the first chunk if its weakly similar
        if len(filtered_docs) == 0 and float(results['distances'][0][0]) < 1.6:
            filtered_docs.append(results['documents'][0][0])

        context = "\n".join(filtered_docs)
        print('Distances:', results['distances'][0])
        #print('Documents:', results['documents'][0])
        #print('Returned Context:', context)
        return context

if __name__ == "__main__":
    retriever = RAGRetriever(collection_name="rag_chunks")

    query = "What date is the midterm for adv machine learning systems??"
    context = retriever.retrieve_v2(query, top_k=3)
    print("Retrieved Context:\n", context)