from app.services.llm_client import LLMClient
from app.services.mock_llm import MockLLMClient
from configs.settings import settings


def create_llm_client() -> LLMClient:
    if settings.llm_provider == "mock":
        return MockLLMClient()

    if settings.llm_provider == "openai":
        from app.services.openai_llm import OpenAILLMClient

        return OpenAILLMClient()

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )