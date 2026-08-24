from pydantic import BaseModel, Field


class MappingEntry(BaseModel):
    entity_type: str
    original_value: str
    replacement_value: str


class MappingRecord(BaseModel):
    mapping_id: str
    entries: list[MappingEntry] = Field(default_factory=list)
