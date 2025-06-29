import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "o4-mini-deep-research-2025-06-26"
SYSTEM_PROMPT = "You are a helpful research assistant."
TOOLS = [{"type": "web_search_preview"}]

client = OpenAI(api_key=OPENAI_API_KEY)


def main() -> None:
    """Run a simple Deep Research query and print the result."""
    system_message = SYSTEM_PROMPT
    question = "What are recent advances in reinforcement learning?"

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "developer",
                "content": [{"type": "input_text", "text": system_message}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": question}],
            },
        ],
        reasoning={"summary": "auto"},
        tools=TOOLS,
    )

    print(response.output[-1].content[0].text)


if __name__ == "__main__":
    main()
