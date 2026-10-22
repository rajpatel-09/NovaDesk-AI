from functools import lru_cache

from langchain.agents import create_agent

from src.agent.tools import search_company_docs
from src.rag.generator import AnswerGenerator

@lru_cache(maxsize=1)
def get_agent():
    llm = AnswerGenerator().llm

    return create_agent(
        model=llm,
        tools=[search_company_docs],
        system_prompt=(
            "You are NovaDesk, an IT helpdesk assistant. "
            "For questions about company policies or IT procedures, "
            "use the search_company_docs tool. "
            "If the request is too vague to understand the problem, "
            "ask a concise clarifying question without calling the tool. "
            "Use company-specific facts only from tool results. "
            "If the tool cannot find relevant information, say so "
            "and do not invent an answer."
        ),
    )

def ask_agent(question: str) -> str:
    result = get_agent().invoke(
        {"messages": [{"role": "user", "content": question}]}
    )

    return result["messages"][-1].content