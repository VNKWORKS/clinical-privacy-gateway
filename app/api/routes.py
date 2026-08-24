from fastapi import APIRouter

from app.schemas.api import DeidentifyRequest, DeidentifyResponse
from app.services.deidentifier import Deidentifier


router = APIRouter(
    prefix="/api/v1",
    tags=["Privacy"],
)

deidentifier = Deidentifier()


@router.post(
    "/deidentify",
    response_model=DeidentifyResponse,
)
def deidentify(request: DeidentifyRequest) -> DeidentifyResponse:
    masked_text, mapping = deidentifier.deidentify(request.text)

    return DeidentifyResponse(
        masked_text=masked_text,
        mapping_id=mapping.mapping_id,
        entities_detected=len(mapping.entries),
    )