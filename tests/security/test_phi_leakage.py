from app.services.gateway import ClinicalPrivacyGateway
from app.services.mock_llm import MockLLMClient


def test_multiple_phi_types_never_reach_llm():
    llm = MockLLMClient()
    gateway = ClinicalPrivacyGateway(llm)

    raw_text = (
        "Patient Marcus Whitfield was born on 14 March 1978 "
        "and lives in Boston. "
        "MRN PCG-4471902. "
        "Account Number: AC-2026-123456. "
        "Health Plan Beneficiary Number: HP-2026-445566. "
        "Email marcus@example.com. "
        "Phone 617-555-0182."
    )

    result = gateway.process(raw_text)

    assert len(llm.received_texts) == 1

    llm_input = llm.received_texts[0]

    sensitive_values = [
        "Marcus Whitfield",
        "14 March 1978",
        "Boston",
        "PCG-4471902",
        "AC-2026-123456",
        "HP-2026-445566",
        "marcus@example.com",
        "617-555-0182",
    ]

    for value in sensitive_values:
        assert value not in llm_input

    assert result["masked_text"] != raw_text
    assert result["final_response"] != result["masked_text"]


def test_phi_is_rehydrated_only_after_llm_processing():
    llm = MockLLMClient()
    gateway = ClinicalPrivacyGateway(llm)

    raw_text = "Marcus Whitfield lives in Boston."

    result = gateway.process(raw_text)

    assert "Marcus Whitfield" not in llm.received_texts[0]
    assert "Boston" not in llm.received_texts[0]

    assert "Marcus Whitfield" in result["final_response"]
    assert "Boston" in result["final_response"]