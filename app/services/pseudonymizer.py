from presidio_analyzer import RecognizerResult

from app.schemas.mapping import MappingEntry, MappingRecord
from app.security.mapping_store import SecureMappingStore


class Pseudonymizer:
    def __init__(self, mapping_store: SecureMappingStore):
        self.mapping_store = mapping_store

    def pseudonymize(
        self,
        text: str,
        entities: list[RecognizerResult],
    ) -> tuple[str, MappingRecord]:
        mapping_id = self.mapping_store.create_mapping_id()

        replacements: dict[tuple[str, str], str] = {}
        counters: dict[str, int] = {}
        entries: list[MappingEntry] = []

        for entity in entities:
            original_value = text[entity.start:entity.end]
            key = (entity.entity_type, original_value)

            if key not in replacements:
                counters[entity.entity_type] = (
                    counters.get(entity.entity_type, 0) + 1
                )

                replacement_value = self._generate_replacement(
                    entity.entity_type,
                    counters[entity.entity_type],
                )

                replacements[key] = replacement_value

                entries.append(
                    MappingEntry(
                        entity_type=entity.entity_type,
                        original_value=original_value,
                        replacement_value=replacement_value,
                    )
                )

        masked_text = self._apply_replacements(
            text,
            entities,
            replacements,
        )

        mapping = MappingRecord(
            mapping_id=mapping_id,
            entries=entries,
        )

        self.mapping_store.save(mapping)

        return masked_text, mapping

    @staticmethod
    def _generate_replacement(
        entity_type: str,
        index: int,
    ) -> str:
        if entity_type == "PERSON":
            return f"Patient_{index:03d}"

        if entity_type == "DATE_TIME":
            return f"DATE_{index:03d}"

        if entity_type == "LOCATION":
            return f"LOCATION_{index:03d}"

        return f"{entity_type}_{index:03d}"

    @staticmethod
    def _apply_replacements(
        text: str,
        entities: list[RecognizerResult],
        replacements: dict[tuple[str, str], str],
    ) -> str:
        masked_text = text

        for entity in sorted(
            entities,
            key=lambda result: result.start,
            reverse=True,
        ):
            original_value = text[entity.start:entity.end]

            replacement_value = replacements[
                (entity.entity_type, original_value)
            ]

            masked_text = (
                masked_text[:entity.start]
                + replacement_value
                + masked_text[entity.end:]
            )

        return masked_text
