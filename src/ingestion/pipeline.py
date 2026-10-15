from src.ingestion.loader import load_company_documents
from src.ingestion.splitter import split_documents
from src.ingestion.embeddings import create_embeddings
from src.ingestion.vectorstore import create_vectorstore

def build_knowledge_base():
    documents = load_company_documents()
    chunks = split_documents(documents)
    embeddings = create_embeddings()
    vectorstore = create_vectorstore(chunks, embeddings)

    return vectorstore

def main():
    vectorstore = build_knowledge_base()
    print(f"Knowledge base created : {vectorstore._collection.count()} chunks")

if __name__ == "__main__":
    main()



