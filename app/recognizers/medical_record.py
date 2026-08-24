from presidio_analyzer import Pattern, PatternRecognizer


class MedicalRecordNumberRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="medical_record_number",
                regex=r"\b(?:MRN|Medical\s+Record\s+Number)\s*[:#-]?\s*[A-Z]{2,10}-[A-Z0-9-]{4,20}\b",
                score=0.95,
            )
        ]

        super().__init__(
            supported_entity="MEDICAL_RECORD_NUMBER",
            patterns=patterns,
            context=[
                "MRN",
                "medical record",
                "medical record number",
                "patient record",
            ],
        )
