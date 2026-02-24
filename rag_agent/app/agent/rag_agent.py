from rag_agent.app.prompt.prompter import Prompter
from rag_agent.app.prompt.retriever import RAGRetriever


class RAGAgent:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.prompter = Prompter()



    def generate_response(self, query):
        context = self.retriever.retrieve(query, top_k=5)
        response = self.prompter.prompt(query, context)
        return response