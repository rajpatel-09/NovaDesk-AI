from langchain_chroma import Chroma

def create_vectorstore(documents, embeddings):
    vectorstore = Chroma(
        persist_directory="data/vector_store",
        collection_name="novadesk_docs",
        embedding_function=embeddings,
    )

    # Find the source files already stored in ChromaDB.
    stored_data = vectorstore.get(include=["metadatas"])

    existing_sources = {
        metadata.get("source")
        for metadata in stored_data["metadatas"]
        if metadata.get("source")
    }

    # Keep only chunks belonging to new source files.
    new_documents = [
        document
        for document in documents
        if document.metadata.get("source") not in existing_sources
    ]

    # Add new chunks without re-adding existing source files.
    if new_documents:
        vectorstore.add_documents(new_documents)

    return vectorstore























