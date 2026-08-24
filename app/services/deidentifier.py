from app.schemas.mapping import MappingRecord
from app.security.mapping_store import SecureMappingStore
from app.services.phi_detector import PHIDetector
from app.services.phi_validator import PHIValidator
from app.services.pseudonymizer import Pseudonymizer


class Deidentifier:
    def __init__(self):
        self.detector = PHIDetector()
        self.validator = PHIValidator()

        self.mapping_store = SecureMappingStore()

        self.pseudonymizer = Pseudonymizer(
            mapping_store=self.mapping_store,
        )

    def deidentify(
        self,
        text: str,
    ) -> tuple[str, MappingRecord]:
        detected_entities = self.detector.analyze(text)

        validated_entities = self.validator.validate(
            detected_entities,
        )

        masked_text, mapping = self.pseudonymizer.pseudonymize(
            text,
            validated_entities,
        )

        return masked_text, mapping
