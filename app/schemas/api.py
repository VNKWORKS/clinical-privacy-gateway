from pydantic import BaseModel, Field


class DeidentifyRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Clinical text that may contain PHI.",
    )


class DeidentifyResponse(BaseModel):
    masked_text: str
    mapping_id: str
    entities_detected: int