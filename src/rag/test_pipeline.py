from src.rag.pipeline import RAGPipeline

def main():
    pipeline = RAGPipeline()

    question = "How can I troubleshoot VPN connection problems?"
    answer = pipeline.ask(question)

    print(f"Question : {question}")
    print(f"\nNovaDesk Answer : {answer}")

if __name__ == "__main__":
    main()
