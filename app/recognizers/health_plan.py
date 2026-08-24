from presidio_analyzer import Pattern, PatternRecognizer


class HealthPlanBeneficiaryRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="health_plan_beneficiary_number",
                regex=r"\b(?:Health\s+Plan\s+Beneficiary\s+Number|Health\s+Plan\s+Member\s+ID|Insurance\s+Member\s+ID|Beneficiary\s+ID)\s*[:#-]?\s*[A-Z0-9]+(?:-[A-Z0-9]+)*\b",
                score=0.95,
            ),
        ]

        super().__init__(
            supported_entity="HEALTH_PLAN_BENEFICIARY_NUMBER",
            patterns=patterns,
            context=[
                "health plan",
                "beneficiary",
                "beneficiary number",
                "member",
                "member id",
                "insurance",
                "policy",
            ],
        )
