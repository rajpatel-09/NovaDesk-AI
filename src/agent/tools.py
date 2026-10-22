from functools import lru_cache
from langchain_core.tools import tool
from src.rag.pipeline import RAGPipeline

@lru_cache(maxsize=1)
def get_rag_pipeline() -> RAGPipeline:
    return RAGPipeline()

@tool
def search_company_docs(question:str) -> str:
        """Search company documents for answers about company policies and IT procedures."""
        return get_rag_pipeline().ask(question)


