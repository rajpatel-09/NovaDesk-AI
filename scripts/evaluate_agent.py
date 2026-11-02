# This script will perform five tasks:
   # 1. Read the JSON evaluation cases.
   # 2. Get the configured AI agent.
   # 3. Send each question to the real agent.
   # 4. Check tool selection, source retrieval, and final-answer keywords.
   # 5. Print an evaluation report.

import json
from pathlib import Path

from src.agent.agent import get_agent

# Find the project root directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Locate the evaluation dataset.
EVALUATION_FILE = PROJECT_ROOT / "evaluation" / "agent_eval_cases.json"

# Reads the JSON file and loads questions.
def load_evaluation_cases():
    """Load evaluation questions from the JSON file."""

    with open(EVALUATION_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# Tests one question and checks its behavior.
def evaluate_case(agent, case):
    """Run one question and evaluate the agent's behavior."""

    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": case["question"]}
            ]
        }
    )

    messages = result["messages"]

    # Collect all tool calls made by the agent.
    actual_tools = []

    for message in messages:
        for tool_call in getattr(message, "tool_calls", []):
            actual_tools.append(tool_call["name"])

    # Check whether the expected tool was selected.
    expected_tool = case["expected_tool"]

    if expected_tool is None:
        tool_passed = len(actual_tools) == 0
    else:
        tool_passed = actual_tools == [expected_tool]

    # Collect results returned by tools.
    tool_results = []

    for message in messages:
        if getattr(message, "type", None) == "tool":
            tool_results.append(str(message.content))

    tool_output = "\n".join(tool_results)

    # Check whether the expected source was retrieved.
    expected_source = case["expected_source"]

    if expected_source is None:
        source_passed = None
    else:
        source_passed = expected_source.lower() in tool_output.lower()

    # Extract the final answer.
    final_answer = str(messages[-1].content) if messages else ""

    # Check whether the expected phrase appears in the answer.
    expected_phrases = case["expected_answer_contains_any"]

    matched_phrase = next(
        (
            phrase
            for phrase in expected_phrases
            if phrase.casefold() in final_answer.casefold()  # Performs case-insensitive text comparison.
        ),
        None,
    )

    answer_passed = matched_phrase is not None

    # Determine the overall result.
    case_passed = (
        tool_passed
        and answer_passed
        and (source_passed is None or source_passed)
    )

    return {
        "case_id": case["case_id"],
        "passed": case_passed,
        "expected_tool": expected_tool,
        "actual_tools": actual_tools,
        "tool_passed": tool_passed,
        "source_passed": source_passed,
        "answer_passed": answer_passed,
        "matched_answer_phrase": matched_phrase,
        "final_answer": final_answer,
    }


def main():
    """Run all evaluation cases and print a report."""

    cases = load_evaluation_cases()

    # Initialize the agent once; get_agent() also uses caching.
    agent = get_agent()

    results = []

    print("\n========== NovaDesk Agent Evaluation ==========\n")

    for case in cases:
        result = evaluate_case(agent, case)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"

        print(f"[{status}] {result['case_id']}")
        print(f"  Expected tool: {result['expected_tool']}")
        print(f"  Actual tools: {result['actual_tools']}")
        print(f"  Tool selection: {result['tool_passed']}")

        if result["source_passed"] is None:
            print("  Source check: N/A")
        else:
            print(f"Source check: {result['source_passed']}")

        print(f"Answer check: {result['answer_passed']}")
        print(f"  Matched phrase: {result['matched_answer_phrase']}")
        print(f"Final answer: {result['final_answer']}\n")

    passed = sum(1 for result in results if result["passed"])
    total = len(results)

    print("============== Evaluation Summary ==============")
    print(f"Total cases: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if total > 0:
        print(f"Success rate: {passed / total * 100:.1f}%")

if __name__ == "__main__":
    main()
