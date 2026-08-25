from app.services.gateway import ClinicalPrivacyGateway
from app.services.mock_llm import MockLLMClient


def test_raw_phi_never_reaches_llm():
    llm = MockLLMClient()
    gateway = ClinicalPrivacyGateway(llm)

    raw_text = "Marcus Whitfield lives in Boston."

    result = gateway.process(raw_text)

    assert result["masked_text"] != raw_text

    assert len(llm.received_texts) == 1

    llm_input = llm.received_texts[0]

    assert "Marcus Whitfield" not in llm_input
    assert "Boston" not in llm_input

    assert "Patient_001" in llm_input
    assert "LOCATION_001" in llm_input


def test_gateway_rehydrates_llm_response():
    llm = MockLLMClient()
    gateway = ClinicalPrivacyGateway(llm)

    raw_text = "Marcus Whitfield lives in Boston."

    result = gateway.process(raw_text)

    assert result["llm_response"] == (
        "Clinical summary: "
        "Patient_001 lives in LOCATION_001."
    )

    assert result["final_response"] == (
        "Clinical summary: "
        "Marcus Whitfield lives in Boston."
    )


def test_gateway_returns_mapping_id():
    llm = MockLLMClient()
    gateway = ClinicalPrivacyGateway(llm)

    result = gateway.process(
        "Marcus Whitfield lives in Boston."
    )

    assert result["mapping_id"]
    assert len(result["mapping_id"]) > 0