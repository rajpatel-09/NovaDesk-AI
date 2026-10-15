from src.rag.retriever import CompanyRetriever
from src.rag.generator import AnswerGenerator

class RAGPipeline:
    def __init__(self, top_k: int = 3):         
        self.retriever = CompanyRetriever(top_k=top_k)
        self.generator = AnswerGenerator()

    def ask(self, question: str) -> str:
        documents = self.retriever.retrieve(question)

        if not documents:
            return "I could not find relevant information in the company documents."

        answer = self.generator.generate_answer(question=question,documents=documents,)

        source_paths = list(
            dict.fromkeys(
                document.metadata.get("source", "Unknown source")
                for document in documents
            )
        )

        sources = "\n".join(f"- {source}" for source in source_paths)

        return (
            f"{answer}\n\n"
            f"Retrieved source documents:\n{sources}"
        )
