from pydantic import BaseModel, Field


class DeidentifyRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Clinical text containing potential PHI.",
    )


class DeidentifyResponse(BaseModel):
    masked_text: str
    mapping_id: str
    entities_detected: int


class ProcessRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Clinical text to securely process.",
    )


class ProcessResponse(BaseModel):
    masked_text: str
    llm_response: str
    final_response: str
    mapping_id: str