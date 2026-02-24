from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Prompter:
    def __init__(self):
        self.client = client
        self.pre_prompt = "You are an assistant that has access to my personal documents." +\
                      "If the question can be answered from your general knowledge, answer directly." +\
                      "If the question requires looking up my documents, answer using the documents provided in CONTEXT below."
        self.model = "gemini-2.5-flash"

    def prompt(self, query: str, context: str = None):
        """
        Send a query to Gemini. If context is provided, it is injected
        into the prompt for RAG-style responses.
        """
        if context:
            full_prompt = (
                f"{self.pre_prompt}\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"QUESTION: {query}"
            )
        else:
            full_prompt = f"{self.pre_prompt}\n\nQUESTION: {query}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt
        )
        return response.text

if __name__ == "__main__":
    query = Prompter()
    print(query.prompt("What is the name of the project I used AWS tools for?"))