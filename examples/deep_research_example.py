import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("DEEP_RESEARCH_MODEL", "o4-mini-deep-research-2025-06-26")
SYSTEM_PROMPT = os.environ.get(
    "DEEP_RESEARCH_SYSTEM_PROMPT", "You are a helpful research assistant."
)
TOOLS = [
    {"type": name} if name != "code_interpreter" else {"type": "code_interpreter", "container": {"type": "auto", "file_ids": []}}
    for name in os.environ.get("DEEP_RESEARCH_TOOLS", "web_search_preview").split(",")
    if name
]

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
