import pytest

from app.schemas.mapping import MappingEntry, MappingRecord
from app.security.mapping_store import (
    MappingNotFoundError,
    SecureMappingStore,
)


def test_mapping_can_be_saved_and_retrieved():
    store = SecureMappingStore()

    mapping = MappingRecord(
        mapping_id="test-mapping-001",
        entries=[
            MappingEntry(
                entity_type="PERSON",
                original_value="Marcus Whitfield",
                replacement_value="Patient_001",
            )
        ],
    )

    store.save(mapping)

    assert store.exists("test-mapping-001")

    loaded = store.get("test-mapping-001")

    assert loaded.mapping_id == "test-mapping-001"
    assert len(loaded.entries) == 1
    assert loaded.entries[0].replacement_value == "Patient_001"


def test_mapping_can_be_deleted():
    store = SecureMappingStore()

    mapping = MappingRecord(
        mapping_id="test-mapping-002",
        entries=[],
    )

    store.save(mapping)

    assert store.exists("test-mapping-002")

    store.delete("test-mapping-002")

    assert not store.exists("test-mapping-002")


def test_missing_mapping_raises_error():
    store = SecureMappingStore()

    with pytest.raises(MappingNotFoundError):
        store.get("missing-mapping")
