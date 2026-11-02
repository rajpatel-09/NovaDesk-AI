# The test_agent.py file contains three unit tests to verify the behavior of our Agentic AI implementation.
# Imagine if modify agent.py tomorrow. Something that worked previously might accidentally break.
# Instead of manually checking everything every time, we run automated tests to catch unexpected changes.
# Your NovaDesk-AI application has three important responsibilities:
        # Search company documents through the RAG pipeline.
        # Pass employee questions to the AI agent and return its final answer.
        # Configure and reuse the agent correctly.

from types import SimpleNamespace # python utility to create an object with attribute without defining entire class

import src.agent.agent as agent_module
import src.agent.tools as tools_module

def test_search_company_docs_uses_rag_pipeline(monkeypatch):  # monkeypatch is a fixture to temporarily replace an attribute or function during a test and restore the original afterward.
    question = "How many casual leave days do employees get?"
    expected_answer = "Employees receive 12 casual leave days per year."

    class FakeRAGPipeline:
        def ask(self, user_question):
            assert user_question == question
            return expected_answer

    fake_pipeline = FakeRAGPipeline()

    monkeypatch.setattr(
        tools_module,
        "get_rag_pipeline",
        lambda: fake_pipeline,
    )

    # invoke() - Execute a LangChain tool or agent.
    result = tools_module.search_company_docs.invoke(
        {"question": question}
    )

    assert result == expected_answer

def test_ask_agent_returns_final_answer(monkeypatch):
    question = "How can I troubleshoot VPN problems?"
    expected_answer = "Check your VPN connection and credentials."

    def fake_invoke(payload):
        assert payload == {
            "messages": [
                {"role": "user", "content": question}
            ]
        }

        return {
            "messages": [
                SimpleNamespace(content=expected_answer)
            ]
        }

    fake_agent = SimpleNamespace(invoke=fake_invoke)

    monkeypatch.setattr(
        agent_module,
        "get_agent",
        lambda: fake_agent,
    )

    answer = agent_module.ask_agent(question)

    assert answer == expected_answer

def test_get_agent_reuses_configured_agent(monkeypatch):
    agent_module.get_agent.cache_clear()

    fake_llm = object()
    fake_created_agent = object()
    create_calls = []

    monkeypatch.setattr(
        agent_module,
        "AnswerGenerator",
        lambda: SimpleNamespace(llm=fake_llm),
    )

    def fake_create_agent(**kwargs):
        create_calls.append(kwargs)
        return fake_created_agent

    monkeypatch.setattr(
        agent_module,
        "create_agent",
        fake_create_agent,
    )

    try:
        first_agent = agent_module.get_agent() # agent first time created and stored in cache
        second_agent = agent_module.get_agent() # returns already created agent
    finally:
        agent_module.get_agent.cache_clear() # clears cache after completing test

    assert first_agent is fake_created_agent  # verify exactly the agent returned that first created
    assert second_agent is first_agent # Checks whether the second call returned the same agent instance as the first call.
    assert len(create_calls) == 1 # Checks whether create_agent() was called only once.

    assert create_calls[0]["model"] is fake_llm # Checks whether the correct LLM was passed when creating the agent.
    assert tools_module.search_company_docs in create_calls[0]["tools"] # Checks whether our company-document search tool was included in the agent's available tools.
    system_prompt = create_calls[0]["system_prompt"] # Extracts the system prompt that was passed during agent creation.

    assert "You are NovaDesk, an IT helpdesk assistant." in system_prompt # Checks whether the agent has been given its correct role.
    assert "ask a concise clarifying question without calling the tool." in system_prompt # Checks whether the prompt instructs the agent to ask for clarification when a question is vague.
    assert "do not invent an answer" in system_prompt # Checks whether the prompt contains the instruction not to make up unsupported answers.