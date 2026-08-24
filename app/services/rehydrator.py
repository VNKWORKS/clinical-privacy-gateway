import re

from app.schemas.mapping import MappingRecord


class Rehydrator:
    def rehydrate(
        self,
        text: str,
        mapping: MappingRecord,
    ) -> str:
        token_to_original = {
            entry.replacement_value: entry.original_value
            for entry in mapping.entries
        }

        if not token_to_original:
            return text

        pattern = re.compile(
            "|".join(
                re.escape(token)
                for token in sorted(
                    token_to_original,
                    key=len,
                    reverse=True,
                )
            )
        )

        return pattern.sub(
            lambda match: token_to_original[match.group(0)],
            text,
        )
