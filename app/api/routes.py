from fastapi import APIRouter

from app.schemas.api import (
    DeidentifyRequest,
    DeidentifyResponse,
    ProcessRequest,
    ProcessResponse,
)
from app.services.deidentifier import Deidentifier
from app.services.gateway import ClinicalPrivacyGateway
from app.services.llm_factory import create_llm_client


router = APIRouter(
    prefix="/api/v1",
    tags=["Privacy"],
)

deidentifier = Deidentifier()

gateway = ClinicalPrivacyGateway(
    create_llm_client(),
)


@router.post(
    "/deidentify",
    response_model=DeidentifyResponse,
)
def deidentify(
    request: DeidentifyRequest,
) -> DeidentifyResponse:
    masked_text, mapping = deidentifier.deidentify(
        request.text,
    )

    return DeidentifyResponse(
        masked_text=masked_text,
        mapping_id=mapping.mapping_id,
        entities_detected=len(mapping.entries),
    )


@router.post(
    "/process",
    response_model=ProcessResponse,
)
def process(
    request: ProcessRequest,
) -> ProcessResponse:
    result = gateway.process(
        request.text,
    )

    return ProcessResponse(
        masked_text=result["masked_text"],
        llm_response=result["llm_response"],
        final_response=result["final_response"],
        mapping_id=result["mapping_id"],
    )