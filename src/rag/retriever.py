from src.ingestion.embeddings import create_embeddings
from src.ingestion.retriever import create_retriever

class CompanyRetriever:
    def __init__(self, top_k : int = 3):
        self.embeddings = create_embeddings()
        self.retriever = create_retriever(self.embeddings)
        self.retriever.search_kwargs["k"] = top_k

    def retrieve(self, question: str):
        return self.retriever.invoke(question)




    
