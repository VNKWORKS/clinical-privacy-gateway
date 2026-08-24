from app.services.phi_detector import PHIDetector


def test_custom_phi_recognizers_are_integrated():
    text = (
        "Marcus Whitfield has MRN PCG-4471902. "
        "Account Number: AC-2026-123456. "
        "Health Plan Member ID: HP-2026-445566."
    )

    results = PHIDetector().analyze(text)

    detected_types = {
        result.entity_type
        for result in results
    }

    assert "PERSON" in detected_types
    assert "MEDICAL_RECORD_NUMBER" in detected_types
    assert "ACCOUNT_NUMBER" in detected_types
    assert "HEALTH_PLAN_BENEFICIARY_NUMBER" in detected_types


def test_existing_presidio_entities_still_work():
    text = (
        "Marcus Whitfield was born on 14 March 1978 "
        "and lives in Boston. "
        "Email marcus@example.com. "
        "Phone 617-555-0182."
    )

    results = PHIDetector().analyze(text)

    detected_types = {
        result.entity_type
        for result in results
    }

    assert "PERSON" in detected_types
    assert "DATE_TIME" in detected_types
    assert "LOCATION" in detected_types
    assert "EMAIL_ADDRESS" in detected_types
    assert "PHONE_NUMBER" in detected_types
