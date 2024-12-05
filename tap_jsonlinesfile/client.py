"""Custom client handling, including JsonLinesFileStream base class."""

from __future__ import annotations

import json
import typing as t
from datetime import datetime
from pathlib import Path

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import Stream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

SYNCED_FILES = "synced_files"


class JsonLinesFileStream(Stream):
    """Stream class for JsonLinesFile streams."""

    def get_records(
        self,
        context: Context | None,
    ) -> t.Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        Iterates over all files matching the search pattern and processes
        each JSON object within the files as a record.

        Args:
            context: Stream partition or context dictionary (not used here).

        Yields:
            Parsed records as dictionaries.
        """
        found_files = self.get_files()
        self.logger.info("Found the following files: %s", found_files)
        unsynced_files = self.filter_already_synced_files(found_files, context)
        self.logger.info("After filtering already synced files: %s", unsynced_files)
        for file in unsynced_files:
            for serial_number, json_obj in enumerate(self.read_file(file)):
                yield self.parse_record(
                    json_obj,
                    file=file,
                    serial_number=serial_number,
                    modified_time=self._get_modified_time(file),
                )

    def filter_already_synced_files(
        self, files: list[Path], context: Context
    ) -> list[Path]:
        """Filter already synced files based on the last modified date."""
        start_timestamp = self.get_starting_timestamp(context)
        if start_timestamp is None:
            return files
        self.logger.info("Starting timestamp %s", start_timestamp)
        return [
            file for file in files if self._get_modified_time(file) > start_timestamp
        ]

    def _get_modified_time(self, file: Path) -> datetime:
        return datetime.fromtimestamp(file.stat().st_mtime)  # noqa: DTZ006

    def parse_record(
        self, json_str: str, file: Path, serial_number: int, modified_time: datetime
    ) -> dict:
        """Parse a record according to the schema and the config.

        Adds source file and serial number to each record, and optionally
        extracts specific fields defined in `variables_to_extract`.

        Args:
            json_str: The raw JSON line from the file.
            file: The name of the source file.
            serial_number: The row number in the file.
            modified_time: the time at which the source file was changed.

        Returns:
            A dictionary representing the parsed record.
        """
        json_obj = json.loads(json_str)
        record = {
            "source_file": str(file),
            "serial_number": serial_number,
            "json_object": json_obj,
            "_modified_time": modified_time,
        }

        variables = self.config.get("variables_to_extract", [])
        for variable in variables:
            column_name = variable["column_name"]
            json_path = variable["path"]
            record[column_name] = self.extract_value(json_obj, json_path)
        return record

    def read_file(self, file: Path) -> t.Iterable[str]:
        """Read a single file and return an iterator over the json array elements."""
        with file.open("rt") as file_handle:
            for line in file_handle:
                yield line.strip()

    def get_files(self) -> list[Path]:
        """Return a list of paths with the files that match the search pattern."""
        path = Path(self.config["path"])
        search_pattern = self.config["search_pattern"]

        if not path.is_dir():
            msg = f"Path does lead to an existing directory: {path}"
            raise ValueError(msg)

        files = list(Path(path).glob(search_pattern))
        if not files:
            msg = (
                f"The given path ({path}) and search pattern ({search_pattern} "
                "do not lead to any files..)"
            )
            raise ValueError(msg)

        return sorted(files, key=lambda file: self._get_modified_time(file))

    def extract_value(self, json_obj: dict, json_path: str) -> t.Any:  # noqa: ANN401
        """Extract a value from a JSON object using a simple JSON path.

        Args:
            json_obj: The JSON object to extract the value from.
            json_path: The JSON path string (dot-separated).

        Returns:
            The extracted value, or None if the path does not exist.
        """
        match list(extract_jsonpath(json_path, json_obj)):
            case [value]:
                return value
            case []:
                return None
            case matches:
                msg = "The given json-path matches multiple values:\n"
                msg += f"{json_path=}\n{matches=}"
                raise ValueError(msg)
