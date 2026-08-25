from presidio_analyzer import RecognizerResult


class PHIValidator:
    def __init__(self, minimum_score: float = 0.50):
        self.minimum_score = minimum_score

        self.identifier_entities = {
            "MEDICAL_RECORD_NUMBER",
            "ACCOUNT_NUMBER",
            "HEALTH_PLAN_BENEFICIARY_NUMBER",
        }

    def validate(
        self,
        results: list[RecognizerResult],
    ) -> list[RecognizerResult]:
        filtered_results = [
            result
            for result in results
            if result.score >= self.minimum_score
        ]

        filtered_results = self._remove_nested_identifier_false_positives(
            filtered_results
        )

        return self._resolve_conflicts(filtered_results)

    def _remove_nested_identifier_false_positives(
        self,
        results: list[RecognizerResult],
    ) -> list[RecognizerResult]:
        identifiers = [
            result
            for result in results
            if result.entity_type in self.identifier_entities
        ]

        if not identifiers:
            return results

        cleaned = []

        for candidate in results:
            if candidate.entity_type in self.identifier_entities:
                cleaned.append(candidate)
                continue

            contained_in_identifier = any(
                self._contained(candidate, identifier)
                for identifier in identifiers
            )

            if not contained_in_identifier:
                cleaned.append(candidate)

        return cleaned

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

    @staticmethod
    def _contained(
        inner: RecognizerResult,
        outer: RecognizerResult,
    ) -> bool:
        return (
            outer.start <= inner.start
            and inner.end <= outer.end
        )