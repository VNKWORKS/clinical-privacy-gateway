from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry

from app.recognizers.account_number import AccountNumberRecognizer
from app.recognizers.health_plan import HealthPlanBeneficiaryRecognizer
from app.recognizers.medical_record import MedicalRecordNumberRecognizer


class PHIDetector:
    def __init__(self):
        registry = RecognizerRegistry()

        registry.load_predefined_recognizers()

        registry.add_recognizer(
            MedicalRecordNumberRecognizer()
        )

        registry.add_recognizer(
            AccountNumberRecognizer()
        )

        registry.add_recognizer(
            HealthPlanBeneficiaryRecognizer()
        )

        self.analyzer = AnalyzerEngine(
            registry=registry,
        )

    def analyze(self, text: str):
        return self.analyzer.analyze(
            text=text,
            language="en",
        )
