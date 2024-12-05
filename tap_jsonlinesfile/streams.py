"""Stream type classes for tap-jsonlinesfile."""

from __future__ import annotations

import typing as t
from importlib import resources

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jsonlinesfile.client import JsonLinesFileStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class JsonLinesFile(JsonLinesFileStream):
    """Define custom stream."""

    name = "json_array_file"
    primary_keys: t.ClassVar[list[str]] = ["source_file", "serial_number"]
    replication_key: t.ClassVar[str] = "_modified_time"
    is_sorted: t.ClassVar[bool] = True

    @property
    def schema(self) -> dict:
        """Dynamically generate the schema based on `variables_to_extract`."""
        variables = self.config.get("variables_to_extract", [])
        properties = [
            th.Property("source_file", th.StringType, description="The source file."),
            th.Property(
                "serial_number",
                th.IntegerType,
                description="nth row from the sourcefile.",
            ),
            *(
                th.Property(
                    var["column_name"],
                    getattr(th, var["type"]),
                    description=f"Extracted value from path: {var['path']}",
                )
                for var in variables
            ),
            th.Property(
                "json_object",
                th.ObjectType(additional_properties=True),
                description="The full JSON object.",
            ),
            th.Property(
                "_modified_time",
                th.DateTimeType,
                description="The modification date of the source file.",
            ),
        ]

        return th.PropertiesList(*properties).to_dict()
