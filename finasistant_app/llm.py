from langchain_anthropic import ChatAnthropic


llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,
    max_tokens=4096,
    max_retries=2,
)

def get_default_anthropic_model():
    return ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        temperature=0,
        max_tokens=4096,
        max_retries=2,
    )
