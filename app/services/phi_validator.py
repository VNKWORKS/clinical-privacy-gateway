from presidio_analyzer import RecognizerResult


class PHIValidator:
    def __init__(self, minimum_score: float = 0.50):
        self.minimum_score = minimum_score

    def validate(
        self,
        results: list[RecognizerResult],
    ) -> list[RecognizerResult]:
        filtered_results = [
            result
            for result in results
            if result.score >= self.minimum_score
        ]

        return self._resolve_conflicts(filtered_results)

    def _resolve_conflicts(
        self,
        results: list[RecognizerResult],
    ) -> list[RecognizerResult]:
        sorted_results = sorted(
            results,
            key=lambda result: (
                -result.score,
                -(result.end - result.start),
                result.start,
            ),
        )

        selected: list[RecognizerResult] = []

        for candidate in sorted_results:
            overlaps = any(
                self._overlaps(candidate, existing)
                for existing in selected
            )

            if not overlaps:
                selected.append(candidate)

        return sorted(
            selected,
            key=lambda result: result.start,
        )

    @staticmethod
    def _overlaps(
        first: RecognizerResult,
        second: RecognizerResult,
    ) -> bool:
        return (
            first.start < second.end
            and second.start < first.end
        )