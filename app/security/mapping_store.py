from uuid import uuid4

from app.schemas.mapping import MappingRecord


class MappingNotFoundError(Exception):
    """Raised when a requested mapping does not exist."""


class SecureMappingStore:
    def __init__(self):
        self._records: dict[str, MappingRecord] = {}

    def create_mapping_id(self) -> str:
        return uuid4().hex

    def save(self, mapping: MappingRecord) -> None:
        self._records[mapping.mapping_id] = mapping

    def get(self, mapping_id: str) -> MappingRecord:
        mapping = self._records.get(mapping_id)

        if mapping is None:
            raise MappingNotFoundError(
                f"Mapping not found: {mapping_id}"
            )

        return mapping

    def delete(self, mapping_id: str) -> None:
        self._records.pop(mapping_id, None)

    def exists(self, mapping_id: str) -> bool:
        return mapping_id in self._records
