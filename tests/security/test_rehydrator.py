from app.schemas.mapping import MappingEntry, MappingRecord
from app.services.rehydrator import Rehydrator


def test_known_tokens_are_rehydrated():
    mapping = MappingRecord(
        mapping_id="mapping-001",
        entries=[
            MappingEntry(
                entity_type="PERSON",
                original_value="Marcus Whitfield",
                replacement_value="Patient_001",
            ),
            MappingEntry(
                entity_type="LOCATION",
                original_value="Boston",
                replacement_value="LOCATION_001",
            ),
        ],
    )

    response = "Patient_001 lives in LOCATION_001."

    result = Rehydrator().rehydrate(
        response,
        mapping,
    )

    assert result == "Marcus Whitfield lives in Boston."


def test_unknown_tokens_are_not_rehydrated():
    mapping = MappingRecord(
        mapping_id="mapping-002",
        entries=[
            MappingEntry(
                entity_type="PERSON",
                original_value="Marcus Whitfield",
                replacement_value="Patient_001",
            ),
        ],
    )

    response = "Patient_001 met Patient_999."

    result = Rehydrator().rehydrate(
        response,
        mapping,
    )

    assert result == "Marcus Whitfield met Patient_999."


def test_clinical_text_is_preserved():
    mapping = MappingRecord(
        mapping_id="mapping-003",
        entries=[
            MappingEntry(
                entity_type="PERSON",
                original_value="Marcus Whitfield",
                replacement_value="Patient_001",
            ),
        ],
    )

    response = (
        "Patient_001 has right L5 radiculopathy "
        "and severe back pain."
    )

    result = Rehydrator().rehydrate(
        response,
        mapping,
    )

    assert (
        result
        == "Marcus Whitfield has right L5 radiculopathy "
        "and severe back pain."
    )
