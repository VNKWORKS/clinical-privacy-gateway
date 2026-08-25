from openai import OpenAI

from configs.settings import settings


class OpenAILLMClient:
    def __init__(self):
        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=settings.openai_api_key,
        )

    def generate(self, text: str) -> str:
        response = self.client.responses.create(
            model=settings.openai_model,
            input=(
                "You are a clinical text processing assistant. "
                "Analyze or summarize the supplied clinical text. "
                "Preserve placeholder tokens exactly as provided. "
                "Do not attempt to infer or reconstruct patient identities. "
                "Return only the useful clinical response.\n\n"
                "Clinical text:\n"
                + text
            ),
        )

        return response.output_text