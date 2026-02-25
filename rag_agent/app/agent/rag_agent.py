from rag_agent.app.prompt.prompter import Prompter
from rag_agent.app.prompt.retriever import RAGRetriever
import time

class RAGAgent:
    def __init__(self):
        self.retriever = RAGRetriever()
        self.prompter = Prompter()



    def generate_response(self, query):
        start_total = time.perf_counter()

        # --- Retrieval timing ---
        start_retrieval = time.perf_counter()
        context = self.retriever.retrieve(query, top_k=5)
        end_retrieval = time.perf_counter()

        # --- LLM / Prompt timing ---
        start_llm = time.perf_counter()
        response = self.prompter.prompt(query, context)
        end_llm = time.perf_counter()

        end_total = time.perf_counter()
        timings = {
            "retrieval_time_ms": (end_retrieval - start_retrieval) * 1000,
            "llm_time_ms": (end_llm - start_llm) * 1000,
            "total_time_ms": (end_total - start_total) * 1000
        }
        print(timings)
        return response

    def generate_response_v2(self, query):
        start_total = time.perf_counter()

        # --- Retrieval timing ---
        start_retrieval = time.perf_counter()
        context = self.retriever.retrieve_v2(query, top_k=5)
        end_retrieval = time.perf_counter()

        # --- LLM / Prompt timing ---
        start_llm = time.perf_counter()
        response = self.prompter.prompt(query, context)
        end_llm = time.perf_counter()

        end_total=time.perf_counter()
        timings = {
            "retrieval_time_ms": (end_retrieval - start_retrieval) * 1000,
            "llm_time_ms": (end_llm - start_llm) * 1000,
            "total_time_ms": (end_total - start_total) * 1000
        }
        print(timings)
        return response
