from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry

from app.recognizers.account_number import AccountNumberRecognizer


def create_analyzer():
    registry = RecognizerRegistry()
    registry.add_recognizer(AccountNumberRecognizer())

    return AnalyzerEngine(registry=registry)


def test_account_number_is_detected():
    analyzer = create_analyzer()

    text = "Account Number: AC-2026-123456"

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "ACCOUNT_NUMBER"
    ]

    assert len(matches) == 1
    assert text[matches[0].start:matches[0].end] == (
        "Account Number: AC-2026-123456"
    )


def test_account_number_alternate_context_is_detected():
    analyzer = create_analyzer()

    text = "Acct No: AC-2026-123456"

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "ACCOUNT_NUMBER"
    ]

    assert len(matches) == 1


def test_unrelated_clinical_identifiers_are_not_account_numbers():
    analyzer = create_analyzer()

    text = (
        "Account / Encounter: ED-24-0211-556. "
        "Claim / Reference: PI-2024-8871. "
        "MRN: PCG-4471902."
    )

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "ACCOUNT_NUMBER"
    ]

    assert matches == []
