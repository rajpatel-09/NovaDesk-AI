from langchain_chroma import Chroma

def cosine_relevance_score(distance: float) -> float:
    """Convert cosine distance into a score between 0 and 1."""

    return max(0.0, min(1.0, 1.0 - distance))

def create_retriever(embeddings):
    vectorstore = Chroma(
        persist_directory="data/vector_store",
        collection_name="novadesk_docs_cosine",
        embedding_function=embeddings,
        relevance_score_fn=cosine_relevance_score,
    )

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.25},
    )
