from __future__ import annotations

from typing import Iterable, List

from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.import_helpers.import_record import ImportRecord


class ImportRecordGroup:
    """
    Grouped by `source` import records for nicer rendering.

    Arguments:
        source -- Common source for import records.
        import_records -- Grouped import records.
    """

    def __init__(
        self, source: ImportString, import_records: Iterable[ImportRecord]
    ) -> None:
        self.source = source
        self.import_records = list(import_records)

    @classmethod
    def from_import_records(
        cls, import_records: Iterable[ImportRecord]
    ) -> List[ImportRecordGroup]:
        """
        Get groups from `ImportRecord` list.

        Arguments:
            import_records -- Import records list.

        Returns:
            A list of generated `ImportRecordGroup`.
        """
        result: List[ImportRecordGroup] = []
        for import_record in sorted(import_records):
            if (
                not result
                or result[-1].source != import_record.source
                or not result[-1].import_records[0].name
                or not import_record.name
            ):
                result.append(ImportRecordGroup(import_record.source, [import_record]))
            else:
                result[-1].import_records.append(import_record)

        return result

    def is_builtins(self) -> bool:
        return self.source.startswith(ImportRecord.builtins_import_string)