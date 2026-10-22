from langchain_chroma import Chroma

def create_retriever(embeddings):
    vectorstore = Chroma(
        persist_directory= "data/vector_store",
        collection_name="novadesk_docs",
        embedding_function=embeddings,
    )

    return vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.25},
    )


