from rag_agent.app.prompt.retriever import RAGRetriever
from rag_agent.app.prompt.prompter import Prompter

retrieval_query = "What unusual quality does the black pocket watch have?"
general_query = "When is lunar new year in 2027"
RAGRetriever = RAGRetriever(collection_name="rag_chunks")
context = RAGRetriever.retrieve(general_query, top_k=5)
#('Context:', context)

gemini = Prompter()
print(gemini.prompt(general_query, context))