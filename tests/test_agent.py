from types import SimpleNamespace

import src.agent.agent as agent_module
import src.agent.tools as tools_module

def test_search_company_docs_uses_rag_pipeline(monkeypatch):
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
        first_agent = agent_module.get_agent()
        second_agent = agent_module.get_agent()
    finally:
        agent_module.get_agent.cache_clear()

    assert first_agent is fake_created_agent
    assert second_agent is first_agent
    assert len(create_calls) == 1

    assert create_calls[0]["model"] is fake_llm
    assert tools_module.search_company_docs in create_calls[0]["tools"]
    system_prompt = create_calls[0]["system_prompt"]

    assert "You are NovaDesk, an IT helpdesk assistant." in system_prompt
    assert "ask a concise clarifying question without calling the tool." in system_prompt
    assert "do not invent an answer" in system_prompt