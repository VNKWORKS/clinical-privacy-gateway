from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry

from app.recognizers.medical_record import MedicalRecordNumberRecognizer


def create_analyzer():
    registry = RecognizerRegistry()
    registry.add_recognizer(MedicalRecordNumberRecognizer())

    return AnalyzerEngine(registry=registry)


def test_medical_record_number_is_detected():
    analyzer = create_analyzer()

    text = "Patient record: MRN PCG-4471902."

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "MEDICAL_RECORD_NUMBER"
    ]

    assert len(matches) == 1
    assert text[matches[0].start:matches[0].end] == "MRN PCG-4471902"


def test_medical_record_number_in_clinical_context():
    analyzer = create_analyzer()

    text = "Whitfield, Marcus D. MRN PCG-4471902"

    results = analyzer.analyze(
        text=text,
        language="en",
    )

    matches = [
        result
        for result in results
        if result.entity_type == "MEDICAL_RECORD_NUMBER"
    ]

    assert len(matches) == 1
    assert text[matches[0].start:matches[0].end] == "MRN PCG-4471902"
