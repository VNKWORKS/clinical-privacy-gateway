from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry

from app.recognizers.health_plan import HealthPlanBeneficiaryRecognizer


def create_analyzer():
    registry = RecognizerRegistry()
    registry.add_recognizer(HealthPlanBeneficiaryRecognizer())

    return AnalyzerEngine(registry=registry)


def test_health_plan_beneficiary_number_is_detected():
    analyzer = create_analyzer()

    text = "Health Plan Beneficiary Number: HP-2026-445566"

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "HEALTH_PLAN_BENEFICIARY_NUMBER"
    ]

    assert len(matches) == 1
    assert text[matches[0].start:matches[0].end] == text


def test_insurance_member_id_is_detected():
    analyzer = create_analyzer()

    text = "Insurance Member ID: HP-2026-445566"

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "HEALTH_PLAN_BENEFICIARY_NUMBER"
    ]

    assert len(matches) == 1


def test_general_insurance_text_is_not_detected():
    analyzer = create_analyzer()

    text = (
        "The patient has health insurance "
        "and is enrolled in the employer health plan."
    )

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "HEALTH_PLAN_BENEFICIARY_NUMBER"
    ]

    assert matches == []
