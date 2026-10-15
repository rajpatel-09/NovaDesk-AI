from src.rag.retriever import CompanyRetriever

def main():
    retriever = CompanyRetriever(top_k=3)

    # question = "How many casual leave days do employees get?"
    question = "How can I troubleshoot VPN connection problems?"
    results = retriever.retrieve(question)

    print(f"Retrieved chunks: {len(results)}")

    for index, document in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(document.page_content)
        print(f"Source: {document.metadata.get('source', 'Unknown')}")


if __name__ == "__main__":
    main()
