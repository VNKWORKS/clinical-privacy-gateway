from app.services.deidentifier import Deidentifier
from app.services.llm_client import LLMClient
from app.services.rehydrator import Rehydrator


class ClinicalPrivacyGateway:
    def __init__(self, llm_client: LLMClient):
        self.deidentifier = Deidentifier()
        self.rehydrator = Rehydrator()
        self.llm_client = llm_client

    def process(self, text: str) -> dict:
        masked_text, mapping = self.deidentifier.deidentify(
            text
        )

        llm_response = self.llm_client.generate(
            masked_text
        )

        final_response = self.rehydrator.rehydrate(
            llm_response,
            mapping,
        )

        return {
            "masked_text": masked_text,
            "llm_response": llm_response,
            "final_response": final_response,
            "mapping_id": mapping.mapping_id,
        }
