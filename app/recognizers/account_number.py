from presidio_analyzer import Pattern, PatternRecognizer


class AccountNumberRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="account_number_full",
                regex=r"\b(?:Account|Acct)\s+(?:Number|No\.?|#)\s*[:#-]?\s*[A-Z0-9]+(?:-[A-Z0-9]+)*\b",
                score=0.95,
            ),
        ]

        super().__init__(
            supported_entity="ACCOUNT_NUMBER",
            patterns=patterns,
            context=[
                "account",
                "account number",
                "account no",
                "account #",
                "acct",
                "billing account",
            ],
        )
