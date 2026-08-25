from app.services.openai_llm import OpenAILLMClient


def test_openai_client_can_be_constructed():
    client = OpenAILLMClient()

    assert client.client is not None