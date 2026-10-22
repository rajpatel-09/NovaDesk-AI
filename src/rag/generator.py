import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

class AnswerGenerator:
    def __init__(self):
        load_dotenv()

        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY is missing from .env")

        self.llm = ChatGroq(
            model = "openai/gpt-oss-20b",
            temperature=0,                       # gives more constant/accurate(the most similar) asnwer rather then creative
            reasoning_format="hidden",           # while asnwering remove the thinking ans give final asnwer bcz model has own thinking
        )

    def generate_answer(self, question:str, documents:list):
        context = "\n\n".join(document.page_content for document in documents)

        message = [
            (
                "system",
                "You are NovaDesk, an IT helpdesk assistant."
                "Answer using only the provided company documents."
                "If the documents do not contain the answer,"
                "say you could not find the information."
                "Do not invent company policies.",
            ),
            (
                "human",
                f"Company documents:\n{context}\n\n"
                f"Employee question: {question}",
            ),
        ]

        response = self.llm.invoke(message)

        return response.content