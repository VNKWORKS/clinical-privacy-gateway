from typing import Protocol


class LLMClient(Protocol):
    def generate(self, text: str) -> str:
        ...


class OpenAILLMClient:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.5",
        timeout: float = 30.0,
    ):
        from openai import OpenAI

        self.client = OpenAI(
            api_key=api_key,
            timeout=timeout,
        )
        self.model = model

    def generate(self, text: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a clinical text assistant. "
                "The input has already been de-identified. "
                "Do not attempt to identify or reconstruct real people. "
                "Provide a useful clinical response while preserving "
                "the supplied pseudonymous identifiers."
            ),
            input=text,
        )

        return response.output_text