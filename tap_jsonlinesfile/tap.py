"""JsonLinesFile tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.helpers.capabilities import TapCapabilities

from tap_jsonlinesfile import streams


class TapJsonLinesFile(Tap):
    """JsonLinesFile tap class."""

    name = "tap-jsonlinesfile"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "entity",
            th.StringType,
            required=True,
            title="Entity",
            description="Target entity name, usually the table name.",
        ),
        th.Property(
            "path",
            th.StringType,
            required=True,
            title="Path",
            description="Path to directory to find jsonl files.",
        ),
        th.Property(
            "search_pattern",
            th.StringType,
            required=True,
            title="Search pattern",
            description="Search pattern to use when discovering files, using glob. Relative to 'path'",
        ),
        th.Property(
            "compression",
            th.StringType,
            title="Compression",
            description="Indicate if the files are compressed. Only support for gz currently.",
        ),
        th.Property(
            "variables_to_extract",
            th.ArrayType(
                th.ObjectType(
                    th.Property(
                        "path",
                        th.StringType,
                        required=True,
                        description="JSONpath expression that maps to the variable.",
                    ),
                    th.Property(
                        "column_name",
                        th.StringType,
                        required=True,
                        description="Column name to assign to the variable.",
                    ),
                    th.Property(
                        "type",
                        th.StringType,
                        required=True,
                        title="Type",
                        description="Singer-sdk typing name, e.g: StringType",
                    ),
                )
            ),
            title="Variables to Extract",
            description=(
                "A list of variables to extract, "
                "each with a JSON path and a column name."
            ),
        ),
    ).to_dict()

    @classproperty
    def capabilities(self) -> list[TapCapabilities]:
        """Get tap capabilites."""
        return [
            TapCapabilities.CATALOG,
            TapCapabilities.DISCOVER,
            TapCapabilities.STATE,
            TapCapabilities.TEST,
        ]

    def discover_streams(self) -> list[streams.JsonLinesFileStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.JsonLinesFile(
                self,
                name=self.config.get("entity"),
            )
        ]


if __name__ == "__main__":
    TapJsonLinesFile.cli()
